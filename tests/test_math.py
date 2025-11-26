import sys
from pathlib import Path
from reverse_loop.tools.calculator import ProfitCalculator

def test_profit_calculator():

    result = ProfitCalculator.claculate_net_profit(100.0, 2.0)

    assert result['net_profit'] == 73.00
    assert result['is_profitable'] == True

def test_neagtive_profit():

    result = ProfitCalculator.claculate_net_profit(10.0, 10.0)

    assert result['net_profit'] < 0
    assert result['is_profitable'] == False