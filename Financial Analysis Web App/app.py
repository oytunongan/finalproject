import requests, json
import helpers
from flask import Flask, render_template, request, redirect, session
from flask_session import Session
import yfinance as yf
from datetime import date
from cs50 import SQL

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///database.db")

headers = {"User-Agent": 'Mozilla/5.0'}
response_ = requests.get("https://www.sec.gov/files/company_tickers.json")

datas = []

def analyze(ticker, symbols=[]):
    for symbol in symbols:
        if symbol[1]["ticker"] == ticker.upper():
            cik = str(symbol[1]["cik_str"]).zfill(10)
            response = requests.get("https://data.sec.gov/api/xbrl/companyfacts/CIK" + cik + ".json", headers=headers)
            values = response.json()
            return values

@app.route("/error")
def error(message, code):
    return render_template("error.html", message=message, code=code)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        ticker = request.form.get("symbol")
        symbols = list(response_.json().items())
        tickers = []
        datas.clear()
        session.clear()

        for symbol in symbols:
            tickers.append(symbol[1]["ticker"])
            if symbol[1]["ticker"] == ticker.upper():
                title = symbol[1]["title"]

        if not ticker:
            return error("Not a valid stock symbol, retry!", 404)
        elif ticker.upper() not in tickers:
            return error("Not a valid stock symbol, retry!", 404)

        for i in range(len(symbols) - 1):
            if not symbols[i][1]["ticker"]:
                return error("Not a valid stock symbol, retry!", 404)

        data= analyze(ticker, symbols)
        summary = dict()
        stock = helpers.Stock(ticker)
        market_price = round(yf.Ticker(ticker).basic_info["lastPrice"], 4)

        # Calculation values collected through Financial Statements

        LiabilityAndEquity = helpers.liability_and_equity(data)
        Equity = helpers.Equity_(data)
        TotalAssets = helpers.Assets(data)
        TotalLiabilities = helpers.Liabilities(data)
        CurrentAssets = helpers.Current_Assets(data)
        CurrentLiabilities = helpers.Current_Liabilities(data)
        Revenue = helpers.Revenue_(data)
        CostOfSales = helpers.CostOfGoods(data)
        OperatingProfits = helpers.Operating_Profits(data)
        NetProfits = helpers.Net_Profits(data)
        Dividends = helpers.Dividends_(data)
        OperatingCash = helpers.Operating_Cash(data)
        InvestingCash = helpers.Investing_Cash(data)
        Shares = helpers.Outstanding_Shares(data)
        InterestExpense = helpers.Interest_Expense(data)
        TotalDebt = helpers.Total_Debt(data)

        # Calculations of Financial Performances

        CR = stock.current_ratio(CurrentAssets, CurrentLiabilities)
        AT = stock.assets_turnover(TotalAssets, Revenue)
        DR = stock.debt_ratio(TotalAssets, TotalLiabilities)
        GPM = stock.Gprofit_margin(Revenue, CostOfSales)
        OPM = stock.Oprofit_margin(Revenue, OperatingProfits)
        NPM = stock.Nprofit_margin(Revenue, NetProfits)
        EPS = stock.EPS(NetProfits, Shares)
        ROA = stock.ROA(NetProfits, TotalAssets)
        ROE = stock.ROE(NetProfits, Equity)
        PE = stock.PE(market_price, EPS)
        MB = stock.MB(market_price, Equity, Shares)
        DP = stock.Dividend_pay(Dividends, Shares)
        FCF = stock.FreeCashFlow(OperatingCash, InvestingCash)
        FSV = stock.StockFutureValue(DP, FCF, InterestExpense, TotalDebt, TotalAssets, TotalLiabilities, Shares)

        summary["CurrentRatio"] = "{:.2f}".format(CR)
        summary["AssetsTurnover"] = "{:.2f}".format(AT)
        summary["DebtRatio"] = "{:.0%}".format(DR)
        summary["GrossProfitMargin"] = "{:.0%}".format(GPM)
        summary["OperatingProfitMargin"] = "{:.0%}".format(OPM)
        summary["NetProfitMargin"] = "{:.0%}".format(NPM)
        summary["ReturnOnInvestment"] = "{:.0%}".format(ROA)
        summary["ReturnOnEquity"] = "{:.0%}".format(ROE)
        summary["P/E"] = "{:.2f}".format(PE)
        summary["Market/Book"] = "{:.2f}".format(MB)
        summary["EarningPerShare"] = "$" + "{:.2f}".format(EPS)
        summary["DividendPayment"] = "$" + "{:.2f}".format(DP)
        summary["StockPotential"] = "{:.0%}".format((FSV / market_price) - 1)
        summary["MarketPrice"] = "$" + "{:.2f}".format(market_price)
        summary["FutureValue"] = "$" + "{:.2f}".format(FSV)

        datas.append(title)
        datas.append(ticker.upper())
        datas.append("{:.2f}".format(FSV))
        datas.append(summary["StockPotential"])

        session["summary"] = summary
        session["stock"] = stock
        session["title"] = title

        return render_template("result.html", summary=summary, stock=stock, title=title)

    elif request.method == "GET":
        return render_template("index.html")

@app.route("/result", methods=["GET", "POST"])
def result():
    if request.method == "POST":
        if request.form.get("shortlist") == "shortlist":
            name = datas[0]
            symbol = datas[1]
            forecast = datas[2]
            potential = datas[3]
            db.execute("INSERT INTO shortlist (stock_name, stock_symbol, stock_estimated_price, stock_potential, search_date) VALUES(?, ?, ?, ?, ?)",
                       name, symbol, forecast, potential, date.today()
                       )
            db.execute("DELETE FROM shortlist WHERE stock_symbol = ?", "")
            return redirect ("/shortlist")
    else:
        try:
            return render_template("result.html", summary=session["summary"], stock=session["stock"], title=session["title"])
        except Exception:
            return redirect ("/")

@app.route("/guide", methods=["GET", "POST"])
def guide():
    if request.method == "POST":
        stock_title = request.form.get("title")
        symbols = list(response_.json().items())
        stock_list = []

        for symbol in symbols:
            stock_list.append(symbol[1])

        for symbol in symbols:
            if stock_title == symbol[1]["title"]:
                stock_ticker = symbol[1]["ticker"]
                session["symbol"] = stock_ticker

        stock_list = sorted(stock_list, key=lambda value: value["title"])

        return render_template("guide.html", stock_list=stock_list, stock_ticker=stock_ticker)

    elif request.method == "GET":
        symbols = list(response_.json().items())
        stock_list = []

        for symbol in symbols:
            stock_list.append(symbol[1])

        stock_list = sorted(stock_list, key=lambda value: value["title"])

        return render_template("guide.html", stock_list=stock_list)

@app.route("/shortlist", methods=["GET", "POST"])
def shortlist():
    if request.method == "POST":
        stock_symbol = request.form.get("stock_symbol")
        data_list = db.execute("SELECT * FROM shortlist WHERE stock_symbol=?", stock_symbol)
        stock_group = db.execute("SELECT stock_symbol FROM shortlist GROUP BY stock_symbol")
        return render_template("shortlist.html", data_list=data_list, stock_group=stock_group)
    else:
        db.execute("DELETE FROM shortlist WHERE stock_symbol = ?", "")
        data_list = db.execute("SELECT * FROM shortlist")
        stock_group = db.execute("SELECT stock_symbol FROM shortlist GROUP BY stock_symbol")
        return render_template("shortlist.html", data_list=data_list, stock_group=stock_group)
