import re

class Stock:
    def __init__(self, stock):
        self.stock = stock.upper()

    def __str__(self):
        return self.stock

    def current_ratio(self, current_assets, current_liabilities):
        try:
            CR = round(current_assets / current_liabilities, 4)
        except ZeroDivisionError:
            CR = 0
        return CR

    def assets_turnover(self, total_assets, revenue):
        try:
            AT = round(revenue / total_assets, 4)
        except ZeroDivisionError:
            AT = 0
        return AT

    def debt_ratio(self, total_assets, total_liabilities):
        try:
            DR = round(total_liabilities / total_assets, 4)
        except ZeroDivisionError:
            DR = 0
        return DR

    def Gprofit_margin(self, revenue, cost_goods):
        try:
            GPM = round((revenue - cost_goods) / revenue, 4)
        except ZeroDivisionError:
            GPM = 0
        return GPM

    def Oprofit_margin(self, revenue, operating_profits):
        try:
            OPM = round(operating_profits / revenue, 4)
        except ZeroDivisionError:
            OPM = 0
        return OPM

    def Nprofit_margin(self, revenue, net_profits):
        try:
            NPM = round(net_profits / revenue, 4)
        except ZeroDivisionError:
            NPM = 0
        return NPM

    def EPS(self, net_profits, outstanding_shares):
        try:
            EPS = round(net_profits / outstanding_shares, 4)
        except ZeroDivisionError:
            EPS = 0
        return EPS

    def ROA(self, net_profits, total_assets):
        try:
            ROA = round(net_profits / total_assets, 4)
        except ZeroDivisionError:
            ROA = 0
        return ROA

    def ROE(self, net_profits, equity):
        try:
            ROE = round(net_profits / equity, 4)
        except ZeroDivisionError:
            ROE = 0
        return ROE

    def PE(self, market_price, EPS):
        if market_price == None:
            market_price = 0
        try:
            PE = round(market_price / EPS, 4)
        except ZeroDivisionError:
            PE = 0
        return PE

    def MB(self, market_price, equity, outstanding_shares):
        if market_price == None:
            market_price = 0
        try:
            MB = round(market_price / (equity / outstanding_shares), 4)
        except ZeroDivisionError:
            MB = 0
        return MB

    def Dividend_pay(self, dividends, outstanding_shares):
        try:
            DP = round(dividends / outstanding_shares, 4)
        except ZeroDivisionError:
            DP = 0
        return DP

    def FreeCashFlow(self, operational_cash, investment_cash):
        FCF = operational_cash - investment_cash
        return FCF

    def StockFutureValue(self, DP, FCF, interest_expense, total_debt, total_assets, total_liabilities, outstanding_shares):
        Value1 = round(DP / 0.054, 4)
        try:
            ri = (interest_expense / total_debt) * (1 - 0.3)
        except ZeroDivisionError:
            try:
                ri = (interest_expense / (total_liabilities * 0.5)) * (1 - 0.3)
            except ZeroDivisionError:
                ri = 0
        ra = (0.5 * ri) + (0.5 * 0.054)
        try:
            Value2 = round(((FCF / ra) - total_debt) / outstanding_shares, 4)
        except ZeroDivisionError:
            Value2 = 0
        try:
            Value3 = round((total_assets - total_liabilities) / outstanding_shares, 4)
        except ZeroDivisionError:
            Value3 = 0
        if Value1 > 0 and Value2 <= 0 and Value3 <= 0:
            FSV = Value1
        elif Value1 <= 0 and Value2 > 0 and Value3 <= 0:
            FSV = Value2
        elif Value1 <= 0 and Value2 <= 0 and Value3 > 0:
            FSV = Value3
        elif Value1 <= 0 and Value2 > 0 and Value3 > 0:
            FSV = round((Value2 + Value3) / 2, 4)
        elif Value2 <= 0 and Value1 > 0 and Value3 > 0:
            FSV = round((Value1 + Value3) / 2, 4)
        elif Value3 <= 0 and Value1 > 0 and Value2 > 0:
            FSV = round((Value1 + Value2) / 2, 4)
        else:
            FSV = round((Value1 + Value2 + Value3) / 3, 4)
        return FSV

def liability_and_equity(data):
    try:
        liabilityANDequity = data["facts"]["us-gaap"]["LiabilitiesAndStockholdersEquity"]["units"]["USD"][len(data["facts"]["us-gaap"]["LiabilitiesAndStockholdersEquity"]["units"]["USD"]) - 1]["val"]
    except Exception:
        try:
            liabilityANDequity = data["facts"]["ifrs-full"]["EquityAndLiabilities"]["units"]["USD"][len(data["facts"]["ifrs-full"]["EquityAndLiabilities"]["units"]["USD"]) - 1]["val"]
        except Exception:
            liabilityANDequity = 0
    return liabilityANDequity
def Equity_(data):
    try:
        equity = data["facts"]["us-gaap"]["StockholdersEquity"]["units"]["USD"][len(data["facts"]["us-gaap"]["StockholdersEquity"]["units"]["USD"]) - 1]["val"]
    except Exception:
        try:
            equity = data["facts"]["us-gaap"]["StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest"]["units"]["USD"][len(data["facts"]["us-gaap"]["StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest"]["units"]["USD"]) - 1]["val"]
        except Exception:
            try:
                equity = data["facts"]["us-gaap"]["PartnersCapitalIncludingPortionAttributableToNoncontrollingInterest"]["units"]["USD"][len(data["facts"]["us-gaap"]["PartnersCapitalIncludingPortionAttributableToNoncontrollingInterest"]["units"]["USD"]) - 1]["val"]
            except Exception:
                try:
                    equity = data["facts"]["ifrs-full"]["Equity"]["units"]["USD"][len(data["facts"]["ifrs-full"]["Equity"]["units"]["USD"]) - 1]["val"]
                except Exception:
                    equity = liability_and_equity(data)
    return equity
def Assets(data):
    try:
        total_assets = data["facts"]["ifrs-full"]["Assets"]["units"]["USD"][len(data["facts"]["ifrs-full"]["Assets"]["units"]["USD"]) - 1]["val"]
    except Exception:
        try:
            total_assets = data["facts"]["us-gaap"]["Assets"]["units"]["USD"][len(data["facts"]["us-gaap"]["Assets"]["units"]["USD"]) - 1]["val"]
        except Exception:
            total_assets = liability_and_equity(data)
    return total_assets
def Liabilities(data):
    try:
        total_liabilities = data["facts"]["ifrs-full"]["Liabilities"]["units"]["USD"][len(data["facts"]["ifrs-full"]["Liabilities"]["units"]["USD"]) - 1]["val"]
    except Exception:
        try:
            total_liabilities = data["facts"]["us-gaap"]["Liabilities"]["units"]["USD"][len(data["facts"]["us-gaap"]["Liabilities"]["units"]["USD"]) - 1]["val"]
        except Exception:
            total_liabilities = liability_and_equity(data) - Equity_(data)
    return total_liabilities
def Current_Assets(data):
    try:
        current_assets = data["facts"]["us-gaap"]["AssetsCurrent"]["units"]["USD"][len(data["facts"]["us-gaap"]["AssetsCurrent"]["units"]["USD"]) - 1]["val"]
    except Exception:
        try:
            current_assets = data["facts"]["us-gaap"]["CashAndCashEquivalentsAtCarryingValue"]["units"]["USD"][len(data["facts"]["us-gaap"]["CashAndCashEquivalentsAtCarryingValue"]["units"]["USD"]) - 1]["val"] + data[
                "facts"]["us-gaap"]["InterestReceivable"]["units"]["USD"][len(data["facts"]["us-gaap"]["InterestReceivable"]["units"]["USD"]) - 1]["val"]
        except Exception:
            try:
                current_assets = data["facts"]["us-gaap"]["CashAndCashEquivalentsAtCarryingValue"]["units"]["USD"][len(data["facts"]["us-gaap"]["CashAndCashEquivalentsAtCarryingValue"]["units"]["USD"]) - 1]["val"]
                for i in range(len(re.findall("(?<=,)[A-Za-z]*?ReceivableNet(?=,)", ",".join(map(str, list(data["facts"]["us-gaap"].keys())))))):
                    current_assets += data["facts"]["us-gaap"][re.findall("(?<=,)[A-Za-z]*?ReceivableNet(?=,)", ",".join(map(str, list(data["facts"]["us-gaap"].keys()))))[i]]["units"]["USD"][len(data["facts"]["us-gaap"][
                        re.findall("(?<=,)[A-Za-z]*?ReceivableNet(?=,)", ",".join(map(str, list(data["facts"]["us-gaap"].keys()))))[i]]["units"]["USD"]) - 1]["val"]
            except Exception:
                try:
                    current_assets = data["facts"]["ifrs-full"][re.findall("(?<=,)CashAndCashEquivalents[a-zA-Z]*?(?=,)", ",".join(map(str, list(data["facts"]["ifrs-full"].keys()))))[0]]["units"]["USD"][len(data["facts"]["ifrs-full"][
                        re.findall("(?<=,)CashAndCashEquivalents[a-zA-Z]*?(?=,)", ",".join(map(str, list(data["facts"]["ifrs-full"].keys()))))[0]]["units"]["USD"]) - 1]["val"]
                    for i in range(len(re.findall("(?<=,)(?![a-zA-Z]*Non)[A-Za-z]*?Receivables(?=,)", ",".join(map(str, list(data["facts"]["ifrs-full"].keys())))))):
                        current_assets += data["facts"]["ifrs-full"][re.findall("(?<=,)(?![a-zA-Z]*Non)[A-Za-z]*?Receivables(?=,)", ",".join(map(str, list(data["facts"]["ifrs-full"].keys()))))[i]]["units"]["USD"][len(data["facts"]["ifrs-full"][
                            re.findall("(?<=,)(?![a-zA-Z]*Non)[A-Za-z]*?Receivables(?=,)", ",".join(map(str, list(data["facts"]["ifrs-full"].keys()))))[i]]["units"]["USD"]) - 1]["val"]
                except Exception:
                    current_assets = round(Assets(data) * 0.5)
    return current_assets
def Current_Liabilities(data):
    try:
        current_liabilities = data["facts"]["us-gaap"]["LiabilitiesCurrent"]["units"]["USD"][len(data["facts"]["us-gaap"]["LiabilitiesCurrent"]["units"]["USD"]) - 1]["val"]
    except Exception:
        try:
            current_liabilities = data["facts"]["us-gaap"]["AccountsPayableAndOtherAccruedLiabilities"]["units"]["USD"][len(data["facts"]["us-gaap"]["AccountsPayableAndOtherAccruedLiabilities"]["units"]["USD"]) - 1]["val"]
            for i in range(len(re.findall("(?<=,)[a-zA-Z]*(?!Current)[a-zA-Z]*?Payable(?=,)", ",".join(map(str, list(data["facts"]["us-gaap"].keys())))))):
                for j in range(len(data["facts"]["us-gaap"][re.findall("(?<=,)[a-zA-Z]*(?!Current)[a-zA-Z]*?Payable(?=,)", ",".join(map(str, list(data["facts"]["us-gaap"].keys()))))[i]]["units"]["USD"])):
                    if re.findall(r"\d\d\d\d-\d\d-\d\d", data["facts"]["us-gaap"][re.findall("(?<=,)[a-zA-Z]*(?!Current)[a-zA-Z]*?Payable(?=,)", ",".join(map(str, list(data[
                        "facts"]["us-gaap"].keys()))))[i]]["units"]["USD"][j]["end"])[0] == "2022-12-31":
                        current_liabilities += data["facts"]["us-gaap"][re.findall("(?<=,)[a-zA-Z]*(?!Current)[a-zA-Z]*?Payable(?=,)", ",".join(map(str, list(data["facts"]["us-gaap"].keys()))))[0]]["units"]["USD"][len(data[
                            "facts"]["us-gaap"][re.findall("(?<=,)[a-zA-Z]*(?!Current)[a-zA-Z]*?Payable(?=,)", ",".join(map(str, list(data["facts"]["us-gaap"].keys()))))[0]]["units"]["USD"]) - 1]["val"]
        except Exception:
            try:
                current_liabilities = 0
                for i in range(len(re.findall("(?<=,)(?![a-zA-Z]*Current)[a-zA-Z]*?Payable[a-zA-Z]*?(?=,)", ",".join(map(str, list(data["facts"]["ifrs-full"].keys())))))):
                    for j in range(len(data["facts"]["ifrs-full"][re.findall("(?<=,)(?![a-zA-Z]*Current)[a-zA-Z]*?Payable[a-zA-Z]*?(?=,)", ",".join(map(str, list(data["facts"]["ifrs-full"].keys()))))[i]]["units"]["USD"])):
                        if re.findall(r"\d\d\d\d-\d\d-\d\d", data["facts"]["ifrs-full"][re.findall("(?<=,)(?![a-zA-Z]*Current)[a-zA-Z]*?Payable[a-zA-Z]*?(?=,)", ",".join(map(str, list(data[
                            "facts"]["ifrs-full"].keys()))))[i]]["units"]["USD"][j]["end"])[0] == "2022-12-31":
                            current_liabilities += data["facts"]["ifrs-full"][re.findall("(?<=,)(?![a-zA-Z]*Current)[a-zA-Z]*?Payable[a-zA-Z]*?(?=,)", ",".join(map(str, list(data["facts"]["ifrs-full"].keys()))))[i]]["units"]["USD"][len(data[
                                "facts"]["ifrs-full"][re.findall("(?<=,)(?![a-zA-Z]*Current)[a-zA-Z]*?Payable[a-zA-Z]*?(?=,)", ",".join(map(str, list(data["facts"]["ifrs-full"].keys()))))[i]]["units"]["USD"]) - 1]["val"]
            except Exception:
                current_liabilities = round(Liabilities(data) * 0.5)
    return current_liabilities
def Revenue_(data):
    try:
        revenue = data["facts"]["us-gaap"]["RevenueFromContractWithCustomerExcludingAssessedTax"]["units"]["USD"][len(data["facts"]["us-gaap"]["RevenueFromContractWithCustomerExcludingAssessedTax"]["units"]["USD"]) - 1]["val"]
    except Exception:
        try:
            revenue = data["facts"]["us-gaap"]["InterestIncomeOperating"]["units"]["USD"][len(data["facts"]["us-gaap"]["InterestIncomeOperating"]["units"]["USD"]) - 1]["val"]
        except Exception:
            try:
                revenue = data["facts"]["us-gaap"][re.findall("(?<=,)(?>Gross)InvestmentIncome.*?(?=,)", ",".join(map(str, list(data["facts"]["us-gaap"].keys()))))[0]]["units"]["USD"][len(data["facts"]["us-gaap"][
                    re.findall("(?<=,)(?>Gross)InvestmentIncome.*?(?=,)", ",".join(map(str, list(data["facts"]["us-gaap"].keys()))))[0]]["units"]["USD"]) - 1]["val"]
            except Exception:
                try:
                    revenue = data["facts"]["us-gaap"][re.findall("(?<=,)Revenue.?(?=,)", ",".join(map(str, list(data["facts"]["us-gaap"].keys()))))[0]]["units"]["USD"][len(data["facts"]["us-gaap"][
                        re.findall("(?<=,)Revenue.?(?=,)", ",".join(map(str, list(data["facts"]["us-gaap"].keys()))))[0]]["units"]["USD"]) - 1]["val"]
                except Exception:
                    try:
                        revenue = data["facts"]["ifrs-full"][re.findall("(?<=,)Revenue.?(?=,)", ",".join(map(str, list(data["facts"]["ifrs-full"].keys()))))[0]]["units"]["USD"][len(data["facts"]["ifrs-full"][
                            re.findall("(?<=,)Revenue.?(?=,)", ",".join(map(str, list(data["facts"]["ifrs-full"].keys()))))[0]]["units"]["USD"]) - 1]["val"]
                    except Exception:
                        revenue = 0
    return revenue
def CostOfGoods(data):
    try:
        cost_goods = data["facts"]["us-gaap"]["CostOfGoodsAndServicesSold"]["units"]["USD"][len(data["facts"]["us-gaap"]["CostOfGoodsAndServicesSold"]["units"]["USD"]) - 1]["val"]
    except Exception:
        try:
            cost_goods = data["facts"]["us-gaap"]["InterestExpense"]["units"]["USD"][len(data["facts"]["us-gaap"]["InterestExpense"]["units"]["USD"]) - 1]["val"]
        except Exception:
            try:
                cost_goods = data["facts"]["ifrs-full"]["CostOfSales"]["units"]["USD"][len(data["facts"]["ifrs-full"]["CostOfSales"]["units"]["USD"]) - 1]["val"]
            except Exception:
                cost_goods = round(Revenue_(data) * 0.7)
    return cost_goods
def Operating_Profits(data):
    try:
        operating_profits = data["facts"]["us-gaap"]["OperatingIncomeLoss"]["units"]["USD"][len(data["facts"]["us-gaap"]["OperatingIncomeLoss"]["units"]["USD"]) - 1]["val"]
    except Exception:
        try:
            operating_profits = data["facts"]["us-gaap"]["IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest"]["units"]["USD"][len(data["facts"]["us-gaap"]["IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest"]["units"]["USD"]) - 1]["val"]
        except Exception:
            try:
                operating_profits = data["facts"]["ifrs-full"]["ProfitLossFromOperatingActivities"]["units"]["USD"][len(data["facts"]["ifrs-full"]["ProfitLossFromOperatingActivities"]["units"]["USD"]) - 1]["val"]
            except Exception:
                operating_profits = 0
    return operating_profits
def Net_Profits(data):
    try:
        net_profits = data["facts"]["us-gaap"]["NetIncomeLoss"]["units"]["USD"][len(data["facts"]["us-gaap"]["NetIncomeLoss"]["units"]["USD"]) - 1]["val"]
    except Exception:
        try:
            net_profits = data["facts"]["ifrs-full"]["ProfitLoss"]["units"]["USD"][len(data["facts"]["ifrs-full"]["ProfitLoss"]["units"]["USD"]) - 1]["val"]
        except Exception:
            net_profits = 0
    return net_profits
def Dividends_(data):
    try:
        dividends = data["facts"]["us-gaap"][re.findall("(?<=,)PaymentsOfDividendsCommonStock(?=,)", ",".join(map(str, list(data["facts"]["us-gaap"].keys()))))[0]]["units"]["USD"][len(data[
            "facts"]["us-gaap"][re.findall("(?<=,)PaymentsOfDividendsCommonStock(?=,)", ",".join(map(str, list(data["facts"]["us-gaap"].keys()))))[0]]["units"]["USD"]) - 1]["val"]
    except Exception:
        try:
            dividends = data["facts"]["us-gaap"][re.findall("(?<=,)PaymentsOfDividends(?=,)", ",".join(map(str, list(data["facts"]["us-gaap"].keys()))))[0]]["units"]["USD"][len(data[
                "facts"]["us-gaap"][re.findall("(?<=,)PaymentsOfDividends(?=,)", ",".join(map(str, list(data["facts"]["us-gaap"].keys()))))[0]]["units"]["USD"]) - 1]["val"]
        except Exception:
            try:
                dividends = data["facts"]["ifrs-full"][re.findall("(?<=,)DividendsPaidClassifiedAsFinancingActivities(?=,)", ",".join(map(str, list(data["facts"]["ifrs-full"].keys()))))[0]]["units"]["USD"][len(data[
                    "facts"]["ifrs-full"][re.findall("(?<=,)DividendsPaidClassifiedAsFinancingActivities(?=,)", ",".join(map(str, list(data["facts"]["ifrs-full"].keys()))))[0]]["units"]["USD"]) - 1]["val"]
            except Exception:
                dividends = 0
    return dividends
def Operating_Cash(data):
    try:
        operating_cash = data["facts"]["us-gaap"]["NetCashProvidedByUsedInOperatingActivities"]["units"]["USD"][len(data["facts"]["us-gaap"]["NetCashProvidedByUsedInOperatingActivities"]["units"]["USD"]) - 1]["val"]
    except Exception:
        try:
            operating_cash = data["facts"]["ifrs-full"]["CashFlowsFromUsedInOperatingActivities"]["units"]["USD"][len(data["facts"]["ifrs-full"]["CashFlowsFromUsedInOperatingActivities"]["units"]["USD"]) - 1]["val"]
        except Exception:
            operating_cash = 0
    return operating_cash
def Investing_Cash(data):
    try:
        investing_cash = data["facts"]["us-gaap"]["NetCashProvidedByUsedInInvestingActivities"]["units"]["USD"][len(data["facts"]["us-gaap"]["NetCashProvidedByUsedInInvestingActivities"]["units"]["USD"]) - 1]["val"]
    except Exception:
        try:
            investing_cash = data["facts"]["ifrs-full"]["CashFlowsFromUsedInInvestingActivities"]["units"]["USD"][len(data["facts"]["ifrs-full"]["CashFlowsFromUsedInInvestingActivities"]["units"]["USD"]) - 1]["val"]
        except Exception:
            investing_cash = 0
    return investing_cash
def Outstanding_Shares(data):
    try:
        outstanding_shares = data["facts"]["dei"]["EntityCommonStockSharesOutstanding"]["units"]["shares"][len(data["facts"]["dei"]["EntityCommonStockSharesOutstanding"]["units"]["shares"]) - 1]["val"]
    except Exception:
        try:
            outstanding_shares = data["facts"]["us-gaap"]["CommonStockSharesOutstanding"]["units"]["shares"][len(data["facts"]["us-gaap"]["CommonStockSharesOutstanding"]["units"]["shares"]) - 1]["val"]
        except Exception:
            try:
                outstanding_shares = data["facts"]["us-gaap"]["WeightedAverageNumberOfSharesOutstandingBasic"]["units"]["shares"][len(data["facts"]["us-gaap"]["WeightedAverageNumberOfSharesOutstandingBasic"]["units"]["shares"]) - 1]["val"]
            except Exception:
                try:
                    outstanding_shares = data["facts"]["us-gaap"]["WeightedAverageLimitedPartnershipUnitsOutstanding"]["units"]["shares"][len(data["facts"]["us-gaap"]["WeightedAverageLimitedPartnershipUnitsOutstanding"]["units"]["shares"]) - 1]["val"]
                except Exception:
                    outstanding_shares = 0
    return outstanding_shares
def Interest_Expense(data):
    try:
        interest_expense = data["facts"]["us-gaap"][re.findall("(?<=,)InterestExpense[a-zA-Z]*?(?=,)", ",".join(map(str, list(data["facts"]["us-gaap"].keys()))))[0]]["units"]["USD"][len(data[
            "facts"]["us-gaap"][re.findall("(?<=,)InterestExpense[a-zA-Z]*?(?=,)", ",".join(map(str, list(data["facts"]["us-gaap"].keys()))))[0]]["units"]["USD"]) - 1]["val"]
    except Exception:
        try:
            interest_expense = data["facts"]["ifrs-full"][re.findall("(?<=,)InterestExpense[a-zA-Z]*?(?=,)", ",".join(map(str, list(data["facts"]["ifrs-full"].keys()))))[0]]["units"]["USD"][len(data[
            "facts"]["ifrs-full"][re.findall("(?<=,)InterestExpense[a-zA-Z]*?(?=,)", ",".join(map(str, list(data["facts"]["ifrs-full"].keys()))))[0]]["units"]["USD"]) - 1]["val"]
        except Exception:
            interest_expense = 0
    return interest_expense
def Total_Debt(data):
    try:
        total_debt = data["facts"]["ifrs-full"][re.findall("(?<=,)LongtermBorrowings(?=,)", ",".join(map(str, list(data["facts"]["ifrs-full"].keys()))))[0]]["units"]["USD"][len(data[
            "facts"]["ifrs-full"][re.findall("(?<=,)LongtermBorrowings(?=,)", ",".join(map(str, list(data["facts"]["ifrs-full"].keys()))))[0]]["units"]["USD"]) - 1]["val"]
    except Exception:
        try:
            total_debt = data["facts"]["us-gaap"][re.findall("(?<=,)SeniorNotes(?=,)", ",".join(map(str, list(data["facts"]["us-gaap"].keys()))))[0]]["units"]["USD"][len(data[
                "facts"]["us-gaap"][re.findall("(?<=,)SeniorNotes(?=,)", ",".join(map(str, list(data["facts"]["us-gaap"].keys()))))[0]]["units"]["USD"]) - 1]["val"] + data[
                "facts"]["us-gaap"][re.findall("(?<=,)ProceedsFromLinesOfCredit(?=,)", ",".join(map(str, list(data["facts"]["us-gaap"].keys()))))[0]]["units"]["USD"][len(data[
                "facts"]["us-gaap"][re.findall("(?<=,)ProceedsFromLinesOfCredit(?=,)", ",".join(map(str, list(data["facts"]["us-gaap"].keys()))))[0]]["units"]["USD"]) - 1]["val"]
        except Exception:
            try:
                total_debt = data["facts"]["us-gaap"][re.findall("(?<=,)OperatingLeaseLiability(?=,)", ",".join(map(str, list(data["facts"]["us-gaap"].keys()))))[0]]["units"]["USD"][len(data[
                    "facts"]["us-gaap"][re.findall("(?<=,)OperatingLeaseLiability(?=,)", ",".join(map(str, list(data["facts"]["us-gaap"].keys()))))[0]]["units"]["USD"]) - 1]["val"]
                for i in range(len(re.findall("(?<=,)LongTermDebt[a-zA-Z]*?(?=,)", ",".join(map(str, list(data["facts"]["us-gaap"].keys())))))):
                    for j in range(len(data["facts"]["us-gaap"][re.findall("(?<=,)LongTermDebt[a-zA-Z]*?(?=,)", ",".join(map(str, list(data["facts"]["us-gaap"].keys()))))[i]]["units"]["USD"])):
                        if re.findall(r"\d\d\d\d", data["facts"]["us-gaap"][re.findall("(?<=,)LongTermDebt[a-zA-Z]*?(?=,)", ",".join(map(str, list(data[
                            "facts"]["us-gaap"].keys()))))[i]]["units"]["USD"][j]["end"])[0] == "2022" and data["facts"]["us-gaap"][re.findall("(?<=,)LongTermDebt[a-zA-Z]*?(?=,)", ",".join(map(str, list(data[
                            "facts"]["us-gaap"].keys()))))[i]]["units"]["USD"][j]["fp"] == "FY":
                            total_debt += data["facts"]["us-gaap"][re.findall("(?<=,)LongTermDebt[a-zA-Z]*?(?=,)", ",".join(map(str, list(data["facts"]["us-gaap"].keys()))))[i]]["units"]["USD"][len(data[
                                "facts"]["us-gaap"][re.findall("(?<=,)LongTermDebt[a-zA-Z]*?(?=,)", ",".join(map(str, list(data["facts"]["us-gaap"].keys()))))[i]]["units"]["USD"]) - 1]["val"]
            except Exception:
                try:
                    total_debt = 0
                    for i in range(len(re.findall("(?<=,)LongTermDebt[a-zA-Z]*?(?=,)", ",".join(map(str, list(data["facts"]["us-gaap"].keys())))))):
                        for j in range(len(data["facts"]["us-gaap"][re.findall("(?<=,)LongTermDebt[a-zA-Z]*?(?=,)", ",".join(map(str, list(data["facts"]["us-gaap"].keys()))))[i]]["units"]["USD"])):
                            if re.findall(r"\d\d\d\d", data["facts"]["us-gaap"][re.findall("(?<=,)LongTermDebt[a-zA-Z]*?(?=,)", ",".join(map(str, list(data[
                                "facts"]["us-gaap"].keys()))))[i]]["units"]["USD"][j]["end"])[0] == "2022" and data["facts"]["us-gaap"][re.findall("(?<=,)LongTermDebt[a-zA-Z]*?(?=,)", ",".join(map(str, list(data[
                                "facts"]["us-gaap"].keys()))))[i]]["units"]["USD"][j]["fp"] == "FY":
                                total_debt += data["facts"]["us-gaap"][re.findall("(?<=,)LongTermDebt[a-zA-Z]*?(?=,)", ",".join(map(str, list(data["facts"]["us-gaap"].keys()))))[i]]["units"]["USD"][len(data[
                                    "facts"]["us-gaap"][re.findall("(?<=,)LongTermDebt[a-zA-Z]*?(?=,)", ",".join(map(str, list(data["facts"]["us-gaap"].keys()))))[i]]["units"]["USD"]) - 1]["val"]
                except Exception:
                    total_debt = round(Liabilities(data) * 0.5)
    return total_debt
