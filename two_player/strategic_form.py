from spark_setup.spark_session import get_spark_session
from pyspark.sql.functions import row_number, lit, col
from pyspark.sql.window import Window
from random import randint, random

from spark_setup.transpose import TransposeDF

def random_strategy_list(l):
    strat_list = list()
    for i in range(l):
        strat_list.append(tuple([randint(0, 100), randint(0, 100), randint(0, 100)]))
    return strat_list

class StrategicForm:
    def __init__(self, payoff_p1, payoff_p2, spark_session):
        """
        payoff_p1 list(tuples): p1 payoff matrix as list of tuples.
        payoff_p1 list(tuples): p1 payoff matrix as list of tuples.
        spark_session 
        """
        columns = [str(i) for i in range(len(payoff_p2[0]))]
        p1 = spark_session.createDataFrame(payoff_p1).toDF(*columns)
        self.payoff_df_p1 = p1.withColumn("strategy_id", row_number().over(Window.orderBy(lit(1))))

        p2 = spark_session.createDataFrame(payoff_p2).toDF(*columns)
        self.payoff_df_p2 = TransposeDF(p2, spark_session)
        self.payoff_df_p2 = self.payoff_df_p2.withColumn("strategy_id", row_number().over(Window.orderBy(lit(1))))

    def get_best_responses(self, ego_player_payoff_matrix, opponent_strategy):
        best_resp_value=list(ego_player_payoff_matrix\
                        .agg({opponent_strategy: 'max'})\
                        .alias("best_resp_value")\
                        .collect()[0].asDict().values())[0]
        return ego_player_payoff_matrix.select('strategy_id').filter(col(opponent_strategy)==best_resp_value)
        
        
if __name__ == "__main__":
    sess = get_spark_session("StrategicForm")
    #payoff_p1 = [(3, 3), (2, 5), (0, 6)]
    #payoff_p2 = [(3, 2), (2, 6), (3, 1)]
    payoff_p1 = random_strategy_list(100)
    payoff_p2 = random_strategy_list(100)
    sf = StrategicForm(payoff_p1, payoff_p2, sess)
    sf.get_best_responses(sf.payoff_df_p2, '0').show()