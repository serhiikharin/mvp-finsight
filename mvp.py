import streamlit as st

# Initialize session state for page tracking
if "page" not in st.session_state:
    st.session_state.page = "login"

# PAGE 1: LOGIN
if st.session_state.page == "login":
    # Create a centered layout with columns
    col1, col2, col3 = st.columns([1, 2, 1])  # Adjust to center col2

    from PIL import Image

    with col2:
        # Load and display a local image
        logo = Image.open("logo.png")
        st.image(logo, width=300)  # Adjust width as needed

        # Centered title
        st.markdown("<h1 style='text-align: center;'>Welcome to FinSight</h1>", unsafe_allow_html=True)

        # Username input (only appears on login page)
        username = st.text_input("Enter your username:")

        # Centered button in columns
        btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 1])
        with btn_col2:
            if st.button("Next"):
                if username:
                    st.session_state.username = username  # Store username
                    st.session_state.page = "dashboard"
                else:
                    st.warning("Please enter your username to continue.")

# PAGE 2: DASHBOARD
elif st.session_state.page == "dashboard":
    st.markdown("<h3 style='text-align: center;'>Pick the subscription you want to start with:</h3>", unsafe_allow_html=True)

    # Updated subscription packages
    subscriptions = {
        "Basic Accounting Tool": "Free tool for financial health monitoring and simple bookkeeping (cash flow, balances, incomes/expenses).",
        "Efficiency Estimation & Guidance": "Context-based advice to improve business efficiency, reduce costs, and find subsidies or tax benefits.",
        "Forecasting & Planning Tool": "Predicts future revenues, expenses, and cash flows using past data and context for scenario planning.",
        "External Factors Advisory": "Analyzes macroeconomic, legal, and political news to recommend strategic business adjustments.",
        "AI Chat Assistant": "Ask financial questions and receive contextual, data-informed advice tailored to your business setup."
    }

    # Display checkboxes for independent subscriptions
    selected_subscriptions = []
    for name, description in subscriptions.items():
        if st.checkbox(name, help=description):
            selected_subscriptions.append(name)

    # Continue button
    if st.button("Continue"):
        if "Basic Accounting Tool" not in selected_subscriptions:
            st.error("You must select the Basic Accounting Tool to proceed.")
        else:
            st.session_state.selected_subscriptions = selected_subscriptions
            st.session_state.page = "next_page"

# PAGE 3: BUSINESS CONTEXT
elif st.session_state.page == "next_page":
    st.markdown("<h3 style='text-align: center;'>Tell us about your business</h3>", unsafe_allow_html=True)

    st.markdown("---")
    # 1. Company Name
    company_name = st.text_input("1. What is the name of your company?")

    st.markdown("---")
    # 2. FTE Size
    fte_options = ["1 FTE", "2–3 FTEs", "4–10 FTEs", "11–30 FTEs", "30+ FTEs"]
    company_size = st.radio("2. What is the size of your company represented in FTEs?", fte_options)

    st.markdown("---")
    # 3. Location Inputs
    st.markdown("3. Where does your business operate (list all relevant regions where your business operates)?")
    hq_city = st.text_input("Headquartered/Registered (city):")
    country = st.text_input("(operates in) Country:")
    regions = st.text_input("(operates in) Regions:")
    cities = st.text_input("(operates in) Cities: (if the whole region is served, insert 'All')")

    st.markdown("---")
    # 4. Legal Form in the Netherlands
    legal_forms = [
        "Eenmanszaak", "Vennootschap onder firma (VOF)", "Besloten vennootschap (BV)",
        "Naamloze vennootschap (NV)", "Stichting", "Coöperatie", "Commanditaire vennootschap (CV)"
    ]
    legal_form = st.selectbox("4. What is the legal form of your business?", legal_forms)

    st.markdown("---")
    # 5. Industry
    industries = [
        "Retail", "Technology", "Finance", "Healthcare", "Hospitality", "Real Estate", "Education",
        "Transportation", "Manufacturing", "Consulting", "Legal", "Marketing", "Creative/Design", "Construction", "Other"
    ]
    selected_industries = st.multiselect("5. What industry do you operate in?", industries)

    st.markdown("---")
   # 6. Revenue with € symbol
    st.markdown("6. What is your approximate yearly revenue?")
    col1, col2 = st.columns([5, 1])
    with col1:
        revenue = st.number_input("", min_value=0, step=1000, label_visibility="collapsed")
    with col2:
        st.markdown("### €")


    # Continue Button to Next Step
    if st.button("Continue to next step"):
        # Optional: Add validation if needed
        if not company_name:
            st.error("Please enter your company name.")
        elif not legal_form:
            st.error("Please select your business legal form.")
        else:
            # Store answers in session_state
            st.session_state.company_info = {
                "name": company_name,
                "fte_size": company_size,
                "hq_city": hq_city,
                "country": country,
                "regions": regions,
                "cities": cities,
                "legal_form": legal_form,
                "industries": selected_industries,
                "revenue": revenue
            }
            st.session_state.page = "final_page"  # move to PAGE 4 or next step

# PAGE 4: PRIVACY POLICY AND PAYMENT
elif st.session_state.page == "final_page":
    company_name = st.session_state.company_info.get("name", "your company")
    fte_size = st.session_state.company_info.get("fte_size", "unknown size")
    selected_subscriptions = st.session_state.get("selected_subscriptions", [])

    # Define pricing based on FTE size
    fte_pricing = {
        "1 FTE": 19,
        "2–3 FTEs": 29,
        "4–10 FTEs": 49,
        "11–30 FTEs": 79,
        "30+ FTEs": 99
    }

    price_per_option = fte_pricing.get(fte_size, 0)
    paid_subs = [s for s in selected_subscriptions if s != "Basic Accounting Tool"]
    total_price = price_per_option * len(paid_subs)

    # Page Title
    st.markdown("<h2 style='text-align: center;'>Privacy Policy and Payment</h2>", unsafe_allow_html=True)

    # Summary
    st.markdown(
        f"""
        <p style='text-align: center;'>
        Thank you <strong>{company_name}</strong>!<br><br>
        It seems that your company has <strong>{fte_size}</strong>.<br>
        For this size of the company, each subscription package costs <strong>{price_per_option}€</strong> per month (apart from the basic one).<br><br>
        You have picked: <strong>{', '.join(selected_subscriptions)}</strong>.<br>
        So your total for now is: <strong>{total_price}€</strong> per month.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # Instruction
    st.markdown("To proceed, accept the terms and conditions and connect your bank for direct debit.")

    # Privacy checkbox with info icon
    col1, col2 = st.columns([0.08, 0.92])
    with col2:
        accept_terms = st.checkbox(
            "I accept the privacy policy and terms and conditions",
            help="By continuing, you agree to the following terms:\n"
             "- We store minimal business/personal data for billing and analysis.\n"
             "- You authorize monthly direct debit from your IBAN.\n"
             "- Subscriptions renew monthly and can be cancelled with one month’s notice.\n"
             "- Your data is never sold or shared with third parties."
        )

    st.markdown("---")

    # Bank connection simulation (real integrations use iDEAL / SEPA or Mollie/Adyen APIs)
    st.markdown("---")

    # Bank connection simulation (real integrations use iDEAL / SEPA or Mollie/Adyen APIs)
    st.markdown("**Connect your bank for direct debit setup:**")

    # Account holder name input
    st.text_input("Account holder full name:", key="account_holder_name")

    # IBAN input
    st.text_input("IBAN (e.g. NL91ABNA0417164300):", key="iban_input")

    # Direct debit consent checkbox
    direct_debit_consent = st.checkbox(
        f"I authorize FinSight to set up a monthly direct debit of {total_price}€ for the selected subscriptions.",
        help="This authorization allows FinSight to automatically collect the monthly subscription fees from your provided IBAN. You can cancel anytime with one month's notice."
    )

    # Continue button
    if st.button("Proceed"):
        if not accept_terms:
            st.error("You must accept the privacy policy and terms to continue.")
        elif not st.session_state.account_holder_name:
            st.error("Please enter the account holder's full name.")
        elif not st.session_state.iban_input:
            st.error("Please provide your IBAN to continue.")
        elif not direct_debit_consent:
            st.error("You must authorize the direct debit to proceed.")
        else:
            st.success("Thank you! Your subscription setup is complete.")
            st.session_state.page = "complete"


# PAGE 5: BANK CONNECTION (CSV SIMULATION)
elif st.session_state.page == "complete":
    st.markdown("<h2 style='text-align: center;'>Connect Your Bank Account</h2>", unsafe_allow_html=True)

    st.markdown(
    """
    <div style='text-align: center;'>
        To enable automatic tracking and analysis of your financial activity,<br>
        please connect your business bank account.<br><br>
        <span style='color: #D35400; font-weight: bold;'>
        Note: For demonstration purposes, there will be an upload of a CSV file of "recent transactions" instead of live bank integration.
        </span>
    </div>
    """,
    unsafe_allow_html=True
    )


    st.markdown("---")

    # Simulated bank selection
    st.markdown("**Select your bank** (simulated):")
    bank = st.selectbox("Choose your bank", ["Select...", "ING", "ABN AMRO", "Rabobank", "Bunq", "SNS Bank", "Other"])

    if bank != "Select...":
        st.success(f"{bank} selected. Ready to connect.")

        # Simulated bank connection field
        st.text_input("Connected account:", value=f"{bank} Business - ***1234", disabled=True)

    # Upload CSV
    st.markdown("**Upload your transaction file (.csv):**")
    uploaded_file = st.file_uploader("Choose a file", type="csv")

    if uploaded_file:
        try:
            import pandas as pd
            df = pd.read_csv(uploaded_file)
            st.session_state.transactions = df  # Store in session for later use
            st.success("Bank connection successful. Transactions synced!")

            # Show a preview of the data
            st.dataframe(df.head())

            # Continue button
            if st.button("Continue to Dashboard"):
                st.session_state.page = "dashboard_main"

        except Exception as e:
            st.error(f"Error reading file: {e}")


# PAGE 6: MAIN DASHBOARD
elif st.session_state.page == "dashboard_main":
    # Set page layout
    st.set_page_config(layout="wide")

    # Center content using three columns
    left_col, center_col, right_col = st.columns([1, 3, 1])  # Adjust ratios if needed

    with center_col:
        st.markdown("<h2 style='text-align: center;'>FinSight Dashboard</h2>", unsafe_allow_html=True)
        st.markdown("---")


    # Define tabs
    tabs = [
        "BASIC ACCOUNTING",
        "EFFICIENCY",
        "PLANNING",
        "EXTERNAL FACTORS",
        "CHAT ASSISTANT"
    ]

    if "active_tab" not in st.session_state:
        st.session_state.active_tab = tabs[0]

    # Center the tab selector using columns
    tab_left, tab_center, tab_right = st.columns([1, 2, 1])
    with tab_center:
        selected_tab = st.radio(
            "Navigation",
            tabs,
            index=tabs.index(st.session_state.active_tab),
            horizontal=True,
            label_visibility="collapsed"
        )

    st.session_state.active_tab = selected_tab

    st.markdown("---")

    # Center the conditional content using columns
    content_left, content_center, content_right = st.columns([1, 3, 1])
    with content_center:
        if selected_tab == "BASIC ACCOUNTING":
            st.subheader("BASIC ACCOUNTING")
            st.info("This section will include financial summary, balance visualizations, and income/expense insights.")
            
            import pandas as pd
            # Ensure transactions are loaded
            if "transactions" in st.session_state:
                df = st.session_state.transactions.copy()

                # Make sure Date column is datetime
                df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

                # Drop rows without valid date
                df = df.dropna(subset=['Date'])

                # Period selection
                period = st.radio("Select time period:", ["Day", "Week", "Month", "Quarter", "Year"], horizontal=True)

                # Grouping rules
                if period == "Day":
                    df['Period'] = df['Date'].dt.date
                elif period == "Week":
                    df['Period'] = df['Date'].dt.to_period("W").apply(lambda r: r.start_time.date())
                elif period == "Month":
                    df['Period'] = df['Date'].dt.to_period("M").astype(str)
                elif period == "Quarter":
                    df['Period'] = df['Date'].dt.to_period("Q").astype(str)
                elif period == "Year":
                    df['Period'] = df['Date'].dt.year

                # Categorize Income vs Expenses (assumes Amount column exists)
                df['Type'] = df['Amount (€)'].apply(lambda x: "Income" if x >= 0 else "Expense")

                # Group by Period and Type
                summary = df.groupby(['Period', 'Type'])['Amount (€)'].sum().unstack(fill_value=0)

                # Calculate Net Income
                summary['Net Income'] = summary.get("Income", 0) + summary.get("Expense", 0)

                # Rename columns for presentation
                summary = summary.rename(columns={"Income": "Total Income", "Expense": "Total Expenses"})

                st.markdown("### Profit & Loss Statement")
                st.dataframe(summary.style.format({"Total Income": "€{:,.2f}", "Total Expenses": "€{:,.2f}", "Net Income": "€{:,.2f}"}))

                # Plot Total Income and Total Expenses
                st.markdown("### Profit & Loss Visualization")
                chart_data = summary[["Total Income", "Total Expenses"]].copy()
                st.bar_chart(chart_data)

                st.markdown("---")  # Separator between bar chart and line chart

                # Cash Flow Line Chart
                cash_flow_data = summary[["Net Income"]].copy()
                import matplotlib.pyplot as plt

                st.markdown("### Cash Flow Over Time")
                fig, ax = plt.subplots(figsize=(10, 4))

                # Plot Net Income as a line
                ax.plot(cash_flow_data.index, cash_flow_data["Net Income"], marker='o', label='Net Income', linewidth=2)

                # Add a pronounced zero line
                ax.axhline(0, color='red', linestyle='--', linewidth=2, label='Zero Line')

                # Styling
                ax.set_xlabel("Period")
                ax.set_ylabel("€")
                ax.set_title("Net Income / Cash Flow Over Time")
                ax.legend()
                ax.grid(True)

                st.pyplot(fig)

                # Group by Period and Category directly using existing Category column
                category_summary = (
                    df.groupby(['Period', 'Category'])['Amount (€)']
                    .sum()
                    .unstack(fill_value=0)
                    .sort_index(axis=1)
                )

                # Display category-based income/expense table
                st.markdown("---")
                st.markdown("### Income & Expense by Category")
                st.dataframe(category_summary.style.format("€{:,.2f}"))
                
                st.markdown("---")

                # Let user choose specific period to visualize
                available_periods = category_summary.index.tolist()
                selected_period = st.selectbox("Select period to visualize category breakdown:", available_periods)

                # Toggle: display percentages or absolute values
                display_mode = st.radio("Display Mode:", ["Percentage", "€ Amount"], horizontal=True)

                # Extract values for selected period
                selected_totals = category_summary.loc[selected_period]
                selected_totals = selected_totals[selected_totals != 0]  # Remove zero entries

                # Optional: colors by income/expense
                colors = ['#2ECC71' if val >= 0 else '#E74C3C' for val in selected_totals]

                # Plot pie chart
                fig, ax = plt.subplots()

                if display_mode == "Percentage":
                    ax.pie(
                        selected_totals.abs(),
                        labels=selected_totals.index,
                        autopct='%1.1f%%',
                        startangle=140,
                        colors=colors,
                        wedgeprops={'edgecolor': 'white'}
                    )
                else:
                    def format_euro(x):
                        return f"€{x:,.0f}"

                    def euro_autopct(pct, allvals):
                        absolute = int(round(pct/100.*sum(allvals)))
                        return format_euro(absolute)

                    ax.pie(
                        selected_totals.abs(),
                        labels=selected_totals.index,
                        autopct=lambda pct: euro_autopct(pct, selected_totals.abs()),
                        startangle=140,
                        colors=colors,
                        wedgeprops={'edgecolor': 'white'}
                    )

                ax.axis('equal')
                st.markdown("### Category Breakdown (Pie Chart)")
                st.pyplot(fig)

                import matplotlib.pyplot as plt

                # Filter for revenue-related transactions
                sales_df = df[df['Category'].str.lower().isin(['revenue', 'sales'])]

                # Group by Period
                sales_summary = sales_df.groupby('Period').agg(
                    sales_Euros=('Amount (€)', 'sum'),
                    sales_Count=('Amount (€)', 'count')
                ).reset_index()

                # Plot
                fig, ax1 = plt.subplots()

                # Bar chart for sales in €
                ax1.bar(sales_summary['Period'], sales_summary['sales_Euros'], color='#3498DB', label="sales (€)")
                ax1.set_xlabel("Period")
                ax1.set_ylabel("sales (€)", color='#3498DB')
                ax1.tick_params(axis='y', labelcolor='#3498DB')

                # Create second y-axis for count
                ax2 = ax1.twinx()
                ax2.plot(sales_summary['Period'], sales_summary['sales_Count'], color='#E74C3C', marker='o', label="sales Count")
                ax2.set_ylabel("Number of sales", color='#E74C3C')
                ax2.tick_params(axis='y', labelcolor='#E74C3C')

                fig.tight_layout()
                st.markdown("---")
                st.markdown("### sales Performance: Revenue vs Number of sales")
                st.pyplot(fig)

            else:
                st.warning("Please upload a transaction file first.")


        elif selected_tab == "EFFICIENCY":
            st.subheader("EFFICIENCY")
            st.info("This section will analyze your costs and suggest optimization tips based on your financial profile.")
            if "Efficiency Estimation & Guidance" not in st.session_state.get("selected_subscriptions", []):
                st.markdown("<h3 style='text-align: center; color: gray;'>🚫 You have not unlocked this feature.</h3>", unsafe_allow_html=True)
            else:
                import pandas as pd
                import streamlit as st
                import matplotlib.pyplot as plt

                if "transactions" in st.session_state:
                    df = st.session_state.transactions.copy()
                    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
                    df = df.dropna(subset=['Date'])
                    df['Amount (€)'] = pd.to_numeric(df['Amount (€)'], errors='coerce')

                    # Extract month/year for custom filtering
                    df['Month'] = df['Date'].dt.month
                    df['Year'] = df['Date'].dt.year

                    # Create user-friendly period selector
                    month_options = {
                        "January": 1,
                        "February": 2,
                        "March": 3,
                        "April": 4,
                        "May": 5,
                        "June": 6,
                        "YTD": "YTD"
                    }

                    selected_period = st.selectbox("Select month to analyze expenses:", list(month_options.keys()))

                    today = pd.Timestamp.today()
                    current_year = today.year

                    # Filter by selected month or YTD
                    if month_options[selected_period] == "YTD":
                        df_filtered = df[df['Year'] == current_year]
                    else:
                        selected_month = month_options[selected_period]
                        df_filtered = df[(df['Year'] == current_year) & (df['Month'] == selected_month)]

                    # Only keep expenses
                    expenses_df = df_filtered[df_filtered['Amount (€)'] < 0]

                    # Group and sort by category
                    expense_summary = (
                        expenses_df.groupby('Category')['Amount (€)']
                        .sum()
                        .abs()
                        .sort_values(ascending=False)
                        .head(5)
                    )

                    # Plot with matplotlib
                    fig, ax = plt.subplots(figsize=(8, 4))
                    bars = ax.bar(expense_summary.index, expense_summary.values, color='#E74C3C')

                    # Add € labels on top
                    for bar in bars:
                        height = bar.get_height()
                        ax.annotate(f"€{height:,.0f}", xy=(bar.get_x() + bar.get_width() / 2, height),
                                    xytext=(0, 5), textcoords="offset points", ha='center', va='bottom', fontsize=10)

                    # Styling
                    ax.set_title("Top 5 Largest Expense Categories", fontsize=14)
                    ax.set_ylabel("Amount (€)")
                    ax.set_xlabel("Category")
                    ax.spines['right'].set_visible(False)
                    ax.spines['top'].set_visible(False)
                    plt.xticks(rotation=15)

                    st.pyplot(fig)

                    st.markdown("---")

                    

                    st.markdown("### Key Financial Ratios (per selected period)")

                    import pandas as pd
                    import streamlit as st
                    import datetime as dt

                    st.markdown("## Key Financial Ratios")

                    # Time frame selector
                    time_frame = st.radio("Select time frame:", ["Week", "Month", "Quarter", "YTD", "Year"], horizontal=True)

                    # Load and clean data
                    df = st.session_state.transactions.copy()
                    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
                    df = df.dropna(subset=['Date'])
                    df['Amount (€)'] = pd.to_numeric(df['Amount (€)'], errors='coerce')

                    # Define filtering logic based on selection
                    today = pd.Timestamp.today()
                    if time_frame == "Week":
                        start_date = today - pd.Timedelta(days=7)
                    elif time_frame == "Month":
                        start_date = today - pd.DateOffset(months=1)
                    elif time_frame == "Quarter":
                        start_date = today - pd.DateOffset(months=3)
                    elif time_frame == "Year":
                        start_date = today - pd.DateOffset(years=1)
                    elif time_frame == "YTD":
                        start_date = pd.Timestamp(today.year, 1, 1)

                    # Filter for selected period
                    df_period = df[df['Date'] >= start_date]

                    # Calculate known components
                    revenue = df_period[df_period['Category'].str.lower() == 'sales']['Amount (€)'].sum()
                    cogs = df_period[df_period['Category'].str.lower().isin(['materials', 'rent', 'utilities', 'Fuel', 'Salaries'])]['Amount (€)'].sum()
                    expenses = df_period[(df_period['Amount (€)'] < 0) & (~df_period['Category'].str.lower().isin(['sales', 'Equipment Purchase']))]['Amount (€)'].sum()
                    spending = expenses  # Same definition
                    income = revenue  # Same definition

                    def display_formula(title, formula, value=None):
                        st.markdown(f"### {title}")
                        st.latex(formula)
                        if value is not None:
                            st.success(f"**Result:** {value}")

                    # 1. Gross Profit Margin
                    if revenue != 0 and not pd.isna(cogs):
                        gp_margin = ((revenue - abs(cogs)) / revenue) * 100
                        display_formula("Gross Profit Margin", r"\frac{Revenue - COGS}{Revenue}", f"{gp_margin:.2f}%")
                    else:
                        display_formula("Gross Profit Margin", r"\frac{Revenue - COGS}{Revenue}")
                    st.markdown("---")

                    # 2. Net Profit Margin
                    if revenue != 0 and not pd.isna(expenses):
                        net_profit = revenue + expenses  # expenses are negative
                        net_margin = (net_profit / revenue) * 100
                        display_formula("Net Profit Margin", r"\frac{Net\ Profit}{Revenue}", f"{net_margin:.2f}%")
                    else:
                        display_formula("Net Profit Margin", r"\frac{Net\ Profit}{Revenue}")
                    st.markdown("---")

                    # 3. Current Ratio
                    display_formula("Current Ratio", r"\frac{Current\ Assets}{Current\ Liabilities}")
                    st.markdown("*This ratio was not calculated because **Current Assets** and **Current Liabilities** are missing. Please provide these to get the result.*")
                    st.markdown("---")

                    # 4. Debt-to-Equity Ratio
                    display_formula("Debt-to-Equity Ratio", r"\frac{Total\ Liabilities}{Shareholders'\ Equity}")
                    st.markdown("*This ratio was not calculated because **Total Liabilities** and **Shareholders' Equity** are missing. Please provide these to get the result.*")
                    st.markdown("---")

                    # 5. Return on Equity (ROE)
                    display_formula("Return on Equity (ROE)", r"\frac{Net\ Income}{Average\ Equity}")
                    st.markdown("*This ratio was not calculated because **Net Income** and **Average Equity** are missing. Please provide these to get the result.*")
                    st.markdown("---")

                    # 6. Inventory Turnover
                    display_formula("Inventory Turnover", r"\frac{COGS}{Average\ Inventory}")
                    st.markdown("*This ratio was not calculated because **Average Inventory** is missing. Please provide this to get the result.*")
                    st.markdown("---")

                    # 7. Accounts Receivable Turnover
                    display_formula("Accounts Receivable Turnover", r"\frac{Net\ Credit\ sales}{Average\ Accounts\ Receivable}")
                    st.markdown("*This ratio was not calculated because **Net Credit sales** and **Average Accounts Receivable** are missing. Please provide these to get the result.*")
                    st.markdown("---")

                    # 8. Spending-to-Income Ratio
                    if income != 0:
                        s2i_ratio = abs(spending) / income
                        display_formula("Spending-to-Income Ratio", r"\frac{Spending}{Income}", f"{s2i_ratio:.2f}")
                    else:
                        display_formula("Spending-to-Income Ratio", r"\frac{Spending}{Income}")
                    st.markdown("---")

                else:
                    st.warning("Upload your transaction data to view insights.")


        elif selected_tab == "PLANNING":
            st.subheader("PLANNING")
            st.info("This section will provide revenue/expense forecasts based on uploaded transactions.")
            if "Forecasting & Planning Tool" not in st.session_state.get("selected_subscriptions", []):
                st.markdown("<h3 style='text-align: center; color: gray;'>🚫 You have not unlocked this feature.</h3>", unsafe_allow_html=True)
            else:
                import pandas as pd
                import matplotlib.pyplot as plt
                from statsmodels.tsa.arima.model import ARIMA

                st.markdown("---")

                if "transactions" in st.session_state:
                    df = st.session_state.transactions.copy()
                    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
                    df = df.dropna(subset=['Date'])

                    # Drop Equipment Purchase and filter for expenses
                    df = df[(df['Amount (€)'] < 0) & (df['Category'].str.lower() != "Equipment Purchase")]

                    # --- UI Toggles ---
                    period_step = st.radio("Forecast based on:", ["Day", "Week", "Month"], horizontal=True)
                    forecast_steps = st.selectbox("Periods to predict ahead:", [1, 2, 3])

                    # --- Grouping based on selected period ---
                    if period_step == "Day":
                        df['Period'] = df['Date'].dt.date
                        freq = 'D'
                    elif period_step == "Week":
                        df['Period'] = df['Date'].dt.to_period("W").apply(lambda r: r.start_time.date())
                        freq = 'W'
                    elif period_step == "Month":
                        df['Period'] = df['Date'].dt.to_period("M").astype(str)
                        freq = 'M'

                    grouped = df.groupby("Period")["Amount (€)"].sum().sort_index()
                    past_series = grouped.astype(float)

                    try:
                        # Fit ARIMA model
                        model = ARIMA(past_series, order=(1, 0, 0))
                        model_fit = model.fit()

                        # Forecast
                        forecast = model_fit.get_forecast(steps=forecast_steps)
                        forecast_values = forecast.predicted_mean
                        conf_int = forecast.conf_int()

                        # Create forecast index
                        if isinstance(past_series.index[0], str):
                            last_date = pd.to_datetime(past_series.index[-1]) + pd.tseries.frequencies.to_offset(freq)
                        else:
                            last_date = pd.to_datetime(past_series.index[-1]) + pd.tseries.frequencies.to_offset(freq)

                        forecast_index = pd.date_range(
                            start=last_date,
                            periods=forecast_steps,
                            freq=freq
                        )

                        # Convert all indexes to datetime for plotting
                        past_index_dt = pd.to_datetime(past_series.index)
                        forecast_index_dt = pd.to_datetime(forecast_index)

                        # --- Plotting ---
                        fig, ax = plt.subplots(figsize=(10, 5))

                        # Plot past values
                        ax.plot(past_index_dt, past_series.values, marker='o', linestyle='-', color='blue', label="Historical Expenses")

                        # Plot forecasted values
                        ax.plot(forecast_index_dt, forecast_values, marker='o', linestyle='dotted', color='orange', label="Forecast")

                        # Plot confidence interval
                        ax.fill_between(forecast_index_dt, conf_int.iloc[:, 0], conf_int.iloc[:, 1], color='orange', alpha=0.3, label="Confidence Interval")

                        # Styling
                        ax.set_title(f"Forecasted Expenses ({period_step}-level)")
                        ax.set_xlabel("Period")
                        ax.set_ylabel("Expenses (€)")
                        ax.legend()
                        ax.grid(True)

                        st.pyplot(fig)

                    except Exception as e:
                        st.error(f"Forecasting failed: {e}")
                else:
                    st.warning("Please upload your transactions first.")

                # --- sales FORECAST (Placed below the expenses forecast) ---

                st.markdown("---")

                # Reuse the same toggles
                if "transactions" in st.session_state:
                    df = st.session_state.transactions.copy()
                    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
                    df = df.dropna(subset=['Date'])

                    # Filter for positive sales values only
                    df = df[(df['Amount (€)'] > 0) & (df['Category'].str.lower() == "sales")]

                    # --- Grouping based on selected period ---
                    if period_step == "Day":
                        df['Period'] = df['Date'].dt.date
                        freq = 'D'
                    elif period_step == "Week":
                        df['Period'] = df['Date'].dt.to_period("W").apply(lambda r: r.start_time.date())
                        freq = 'W'
                    elif period_step == "Month":
                        df['Period'] = df['Date'].dt.to_period("M").astype(str)
                        freq = 'M'

                    grouped = df.groupby("Period")["Amount (€)"].sum().sort_index()
                    sales_series = grouped.astype(float)

                    try:
                        # Fit ARIMA model
                        model = ARIMA(sales_series, order=(1, 0, 0))
                        model_fit = model.fit()

                        # Forecast
                        forecast = model_fit.get_forecast(steps=forecast_steps)
                        forecast_values = forecast.predicted_mean
                        conf_int = forecast.conf_int()

                        # Create forecast index
                        if isinstance(sales_series.index[0], str):
                            last_date = pd.to_datetime(sales_series.index[-1]) + pd.tseries.frequencies.to_offset(freq)
                        else:
                            last_date = pd.to_datetime(sales_series.index[-1]) + pd.tseries.frequencies.to_offset(freq)

                        forecast_index = pd.date_range(
                            start=last_date,
                            periods=forecast_steps,
                            freq=freq
                        )

                        # Convert all indexes to datetime for plotting
                        sales_index_dt = pd.to_datetime(sales_series.index)
                        forecast_index_dt = pd.to_datetime(forecast_index)

                        # --- Plotting ---
                        fig, ax = plt.subplots(figsize=(10, 5))

                        # Plot past values
                        ax.plot(sales_index_dt, sales_series.values, marker='o', linestyle='-', color='blue', label="Historical sales")

                        # Plot forecasted values
                        ax.plot(forecast_index_dt, forecast_values, marker='o', linestyle='dotted', color='orange', label="Forecast")

                        # Plot confidence interval
                        ax.fill_between(forecast_index_dt, conf_int.iloc[:, 0], conf_int.iloc[:, 1], color='orange', alpha=0.3, label="Confidence Interval")

                        # Styling
                        ax.set_title(f"Forecasted sales ({period_step}-level)")
                        ax.set_xlabel("Period")
                        ax.set_ylabel("sales (€)")
                        ax.legend()
                        ax.grid(True)

                        st.pyplot(fig)

                    except Exception as e:
                        st.error(f"sales forecasting failed: {e}")
                else:
                    st.warning("Please upload your transactions first.")

                st.markdown("---")



        elif selected_tab == "EXTERNAL FACTORS":
            st.subheader("EXTERNAL FACTORS")
            st.info("This section will track external news and macroeconomic factors affecting your business.")
            if "External Factors Advisory" not in st.session_state.get("selected_subscriptions", []):
                st.markdown("<h3 style='text-align: center; color: gray;'>🚫 You have not unlocked this feature.</h3>", unsafe_allow_html=True)
            else:
                st.markdown(
                "<div style='text-align: center; color: gray; font-size: 23px;'>"
                "🤖 This feature is currently under development and will be available in a future update."
                "</div>",
                unsafe_allow_html=True
                )

        elif selected_tab == "CHAT ASSISTANT":
            st.subheader("CHAT ASSISTANT")
            st.info("This section will host an interactive assistant for financial queries (optional for MVP).")
            st.markdown(
                "<div style='text-align: center; color: gray; font-size: 23px;'>"
                "🤖 This feature is currently under development and will be available in a future update."
                "</div>",
                unsafe_allow_html=True
            )
