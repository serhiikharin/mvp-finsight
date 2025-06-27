# FinSight MVP – AI Financial Advisor for SMEs

This is the Minimum Viable Product (MVP) for **FinSight**, a financial advisory platform designed for small and medium-sized enterprises (SMEs) -- with implementation of AI (excluded in the MVP). It provides a modular and user-friendly solution for financial analysis, forecasting, efficiency optimization, and contextual insights.

---

## Technologies Used

- **Programming Language**: Python
- **Framework**: Streamlit (frontend + backend)
- **Data Handling**: pandas
- **Forecasting Models**: ARIMA (via `statsmodels`) -- only basic predicion models in MVP 
- **Visualization**: matplotlib, Streamlit built-in charts
- **App Type**: Web-based GUI (Single-page, multi-step)

---

## How to Run Locally

1. **Install dependencies**:
   ```bash
   pip install streamlit pandas matplotlib statsmodels
2. Run the app:
   ```bash
   streamlit run mvp.py


## Client company simulation
To demonstrate the functionality of the product and different website pages, there was a mock company named "EnConstruct" simulated. This is a company that is located in the Netherlands and provides renovations and energy solutions for private houses. It is a small local company that has 18 FTEs. For the demonstration purposes, only company's bank transactions will be used -- for simplicity. The transactions simulated were created by ChatGPT and only represent period between March and June. 

## Website navigation 
The first page of the website is a "Welcome" and login page (in MVP, simplified for convenience). 

On the next page, the packages are picked by the client. By hovering over the "i" icon, more details about the package can be found. At least the basic package (free) has to be selected to proceed. Packages can be purchased independently. Client pays for only what they pick. 

On the next page, more basic context is required about the firm: name, size (in FTEs -- price depends on the size of the company), where the company is located and where it operates, the legal form of the business, industry of the business, and approximate annual revenue. Filling in company name and size is mandatory fields. All of these are collected to then provide advice that is closest to the client's company. 

On the next page, the summary of packages selected and the price to be paid (based on packages selected and a company size) is presented. The terms and conditions have to be accepted at this point (more information by hovering over the "i" icon -- basic privacy rules and payment requirements). Also below is the bank information to set up a direct debit to access the main functionality and activate the subscription to the service. Tick a box to authorise payment. All of the fields are required. 

On the next page the bank of the client will be connected -- for synchronizing the transfers and information about company's incomes and expenses. However, for the demonstration purposes and simplicity, the simulated transaction data will be used from the fictitious company (EcConstruct). After connecting the bank, the client can proceed to the dashboards. 

Here, there are 5 tabs with each representing one package. if the package was not chosen during setup (and not paid for), it will display "🚫 You have not unlocked this feature." In some cases (as with AI assistant) for the MVP purposes it says "🤖 This feature is currently under development and will be available in a future update." because it was excluded from the MVP but will be available on the full product. 

Basic accounting feature is always available. THere are: P&L statement, P&L graph, cash flow graph, table that categorizes incomes and expenses. The scale of these reports and visualizations can be adjusted by the toggle on the top of the page (days, weeks, months, quarters, years). Lower down there is a pie chart illustration of the cash flows, here it can be picked for what period should it be displayed (within the scale that has been selected at the top of the page, eg. in months -- each month can be selected to be illustrated). Also it can be chosen if the values should be illustrated in euros or percentage. Lower there is a bar chart where bars represent sales (per scale selected before) in total revenue, while the line illustrates sales in amount of transactions per period. 

Next tab, Efficiency, illustrates at the top the graph with highest expenses for the selected month (or from the beginning of year till today). Lower down, there are basic financial ratios. Some of them present results because they could be estimated with bank statement provided before, while others dont show numeric values but specify what information should be added to the program to estimate the values (the same information can be used in other domains -- or packages -- of the system). 

In the Planning package, the very basic prediction (ARIMA autoregression of expenses/sales) demonstrates the projection of the next period expenses and sales. Here, toggles can adjust the scale of forecast (in days, weeks, months) and how much periods ahead should it predict the values (1-3). 

These are the basic features that were developed for the MVP to demonstrate very elementary functionality of the service. Some packages (AI assistant) were not developed and excluded from the MVP due to complexity of development, while some more complex information in the existing packages was also excluded from the MVP to simplify the demonstration. The website itself is quite basic in its design, but only is such for the MVP. 

---

## Repository Info
**Topic Tags**: `fintech` `ai` `sme` `streamlit` `forecasting` `financial-planning`  
**Description**: MVP for FinSight – AI-powered financial advisory platform for SMEs.
