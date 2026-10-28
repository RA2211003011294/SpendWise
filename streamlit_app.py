
import os
from datetime import date, datetime, timedelta

import pandas as pd
import requests
import streamlit as st


# =========================================================
# CONFIGURATION
# =========================================================

API_URL = os.getenv(
    "SPENDWISE_API_URL",
    "http://127.0.0.1:8000",
).rstrip("/")

st.set_page_config(
    page_title="SpendWise | Finance Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# STYLING
# =========================================================


# =========================================================
# PREMIUM SPENDWISE DESIGN
# =========================================================

st.markdown(
    """
    <style>
    /* ---------- Overall application ---------- */
    .stApp {
        background: #F4F7FC;
        color: #172033;
        font-family: "Inter", "Segoe UI", sans-serif;
    }

    .block-container {
        max-width: 1450px;
        padding: 2rem 2.5rem 3rem;
    }

    /* ---------- Sidebar ---------- */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111B32 0%, #1B2945 100%);
        border-right: 1px solid #243653;
    }

    [data-testid="stSidebar"] * {
        color: #E8EEF9;
    }

    [data-testid="stSidebar"] h1 {
        color: #FFFFFF !important;
        font-size: 1.65rem;
        font-weight: 800;
    }

    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        color: #A5B4CF !important;
    }

    [data-testid="stSidebar"] hr {
        border-color: #35435C;
        margin: 1.5rem 0;
    }

    [data-testid="stSidebar"] [role="radiogroup"] label {
        background: transparent;
        border-radius: 9px;
        padding: 8px 10px;
        transition: background 0.2s ease;
    }

    [data-testid="stSidebar"] [role="radiogroup"] label:hover {
        background: #293955;
    }

    /* ---------- Main headings ---------- */
    .brand-title {
        font-size: 2.55rem;
        font-weight: 800;
        letter-spacing: -1.2px;
        line-height: 1.2;
        color: #14213D !important;
        margin: 0 0 5px 0;
    }

    .brand-subtitle {
        font-size: 1rem;
        color: #71809A !important;
        margin: 0 0 1.7rem 0;
    }

    .stApp h1,
    .stApp h2,
    .stApp h3 {
        color: #172033 !important;
        letter-spacing: -0.35px;
    }

    .stApp h2 {
        font-size: 1.45rem;
        font-weight: 750;
    }

    .stApp h3 {
        font-size: 1.12rem;
        font-weight: 700;
    }

    .stApp p,
    .stApp label,
    .stApp [data-testid="stWidgetLabel"] p {
        color: #475569;
    }

    /* ---------- Metric cards ---------- */
    div[data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #E7ECF4;
        border-radius: 16px;
        padding: 22px 20px;
        min-height: 130px;
        box-shadow: 0 4px 16px rgba(26, 44, 78, 0.045);
        transition: transform 0.2s ease,
                    box-shadow 0.2s ease;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 22px rgba(26, 44, 78, 0.09);
    }

    div[data-testid="stMetric"] label {
        color: #71809A !important;
        font-size: 0.88rem;
        font-weight: 600;
    }

    div[data-testid="stMetricValue"] {
        color: #14213D !important;
        font-size: 1.85rem;
        font-weight: 800;
    }

    div[data-testid="stMetricDelta"] {
        font-size: 0.78rem;
    }

    /* ---------- Buttons ---------- */
    .stApp .stButton > button,
    .stApp .stFormSubmitButton > button,
    .stApp .stDownloadButton > button {
        border-radius: 10px;
        border: 1px solid #2563EB;
        background: #2563EB;
        color: #FFFFFF !important;
        font-weight: 650;
        padding: 0.62rem 1rem;
        min-height: 42px;
        transition: all 0.2s ease;
    }

    .stApp .stButton > button:hover,
    .stApp .stFormSubmitButton > button:hover,
    .stApp .stDownloadButton > button:hover {
        background: #1D4ED8;
        border-color: #1D4ED8;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
    }

    /* ---------- Inputs ---------- */
    .stApp input,
    .stApp textarea {
        background: #FFFFFF !important;
        color: #172033 !important;
        border-radius: 9px !important;
        border-color: #D9E1ED !important;
    }

    .stApp input::placeholder,
    .stApp textarea::placeholder {
        color: #94A3B8 !important;
        opacity: 1;
    }

    .stApp [data-baseweb="select"] > div {
        background: #FFFFFF;
        border-color: #D9E1ED;
        border-radius: 9px;
    }

    /* ---------- Tabs ---------- */
    .stApp button[data-baseweb="tab"] {
        color: #64748B !important;
        font-weight: 600;
    }

    .stApp button[data-baseweb="tab"][aria-selected="true"] {
        color: #2563EB !important;
    }

    /* ---------- Containers and tables ---------- */
    [data-testid="stDataFrame"] {
        background: #FFFFFF;
        border: 1px solid #E7ECF4;
        border-radius: 12px;
        overflow: hidden;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        border-color: #E1E8F2;
        border-radius: 14px;
    }

    /* ---------- Alerts ---------- */
    [data-testid="stAlert"] {
        border-radius: 12px;
    }

    /* ---------- Dividers and captions ---------- */
    .stApp hr {
        border-color: #E3E9F2;
        margin: 1.5rem 0;
    }

    .stApp [data-testid="stCaptionContainer"] {
        color: #8190A7;
    }

    /* ---------- Charts ---------- */
    [data-testid="stVegaLiteChart"],
    [data-testid="stArrowVegaLiteChart"] {
        background: #FFFFFF;
        border: 1px solid #E7ECF4;
        border-radius: 14px;
        padding: 10px;
    }

    /* ---------- Download buttons ---------- */
    .stApp .stDownloadButton > button {
        width: 100%;
    }

    /* ---------- Smaller screens ---------- */
    @media (max-width: 768px) {
        .block-container {
            padding: 1.2rem 1rem 2rem;
        }

        .brand-title {
            font-size: 2rem;
        }

        div[data-testid="stMetric"] {
            padding: 14px;
            min-height: 110px;
        }

        div[data-testid="stMetricValue"] {
            font-size: 1.35rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)



# =========================================================
# SESSION STATE
# =========================================================

defaults = {
    "token": None,
    "email": None,
    "notice": None,
    "confirm_delete": None,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# API CLIENT
# =========================================================

class APIError(Exception):
    pass


def api_request(method, endpoint, **kwargs):
    """Make an authenticated request to the FastAPI backend."""

    headers = kwargs.pop("headers", {}).copy()

    if st.session_state.token:
        headers["Authorization"] = (
            f"Bearer {st.session_state.token}"
        )

    try:
        response = requests.request(
            method,
            f"{API_URL}{endpoint}",
            headers=headers,
            timeout=15,
            **kwargs,
        )
    except requests.RequestException as exc:
        raise APIError(
            f"Cannot connect to the backend at {API_URL}. "
            "Check that FastAPI is running."
        ) from exc

    if response.status_code in (401, 403):
        st.session_state.token = None
        st.session_state.email = None
        raise APIError(
            "Your session expired or access was denied. "
            "Please log in again."
        )

    if not response.ok:
        try:
            detail = response.json().get(
                "detail", response.text
            )
        except (ValueError, AttributeError):
            detail = response.text

        raise APIError(
            f"API error {response.status_code}: {detail}"
        )

    if response.status_code == 204 or not response.content:
        return None

    try:
        return response.json()
    except ValueError:
        return response.text


def extract_expenses(data):
    """Support common FastAPI list response formats."""

    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        for key in ("items", "expenses", "results", "data"):
            if isinstance(data.get(key), list):
                return data[key]

    raise APIError(
        "Unexpected response from /expenses. "
        "Expected a list of expense records."
    )


def money(value):
    try:
        return f"₹{float(value):,.2f}"
    except (TypeError, ValueError):
        return "₹0.00"


def notify(kind, message):
    st.session_state.notice = (kind, message)


def show_notice():
    notice = st.session_state.notice

    if notice:
        st.session_state.notice = None
        kind, message = notice

        if kind == "success":
            st.success(message)
        elif kind == "error":
            st.error(message)
        else:
            st.info(message)


# =========================================================
# DATA PROCESSING
# =========================================================

def load_expenses():
    """Fetch the current user's expenses from the API."""

    response = api_request("GET", "/expenses")
    records = extract_expenses(response)

    df = pd.DataFrame(records)

    required_columns = [
        "id",
        "amount",
        "category",
        "description",
        "expense_date",
    ]

    for column in required_columns:
        if column not in df.columns:
            if column == "id" and not df.empty:
                raise APIError(
                    "Expense records need an id field "
                    "for editing and deleting."
                )
            df[column] = pd.Series(dtype="object")

    if not df.empty:
        df["amount"] = pd.to_numeric(
            df["amount"], errors="coerce"
        ).fillna(0)

        df["expense_date"] = pd.to_datetime(
            df["expense_date"], errors="coerce"
        )

        df["category"] = (
            df["category"].fillna("Other").astype(str)
        )

        df["description"] = (
            df["description"].fillna("").astype(str)
        )

    return df


def filter_expenses(df, start_date, end_date, category="All"):
    """Filter records by date and category."""

    if df.empty:
        return df.copy()

    result = df.copy()

    result = result[
        result["expense_date"].notna()
        & result["expense_date"].dt.date.between(
            start_date, end_date
        )
    ]

    if category != "All":
        result = result[result["category"] == category]

    return result


def period_total(df):
    if df.empty:
        return 0.0
    return float(df["amount"].sum())


def previous_period(start_date, end_date):
    """Return an equally long period immediately before the current one."""

    number_of_days = (end_date - start_date).days + 1

    previous_end = start_date - timedelta(days=1)
    previous_start = previous_end - timedelta(
        days=number_of_days - 1
    )

    return previous_start, previous_end


def display_dataframe(df):
    """Prepare readable dates and currency values for tables."""

    result = df.copy()

    if "expense_date" in result.columns:
        result["expense_date"] = (
            result["expense_date"].dt.strftime("%Y-%m-%d")
        )

    if "amount" in result.columns:
        result["amount"] = result["amount"].map(money)

    result = result.rename(
        columns={
            "id": "ID",
            "expense_date": "Date",
            "category": "Category",
            "description": "Description",
            "amount": "Amount",
        }
    )

    preferred = [
        "ID", "Date", "Category", "Description", "Amount"
    ]

    return result[
        [column for column in preferred if column in result.columns]
    ]


# =========================================================
# AUTHENTICATION
# =========================================================

def authentication_page():
    st.markdown(
        '<p class="brand-title">💰 SpendWise</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="brand-subtitle">'
        'Understand your spending. Make smarter decisions.'
        '</p>',
        unsafe_allow_html=True,
    )

    _, center, _ = st.columns([1, 1.3, 1])

    with center:
        login_tab, register_tab = st.tabs(
            ["Login", "Create account"]
        )

        with login_tab:
            st.subheader("Welcome back")

            with st.form("login_form"):
                email = st.text_input(
                    "Email",
                    placeholder="you@example.com",
                )
                password = st.text_input(
                    "Password",
                    type="password",
                )

                submitted = st.form_submit_button(
                    "Login",
                    use_container_width=True,
                )

            if submitted:
                if not email.strip() or not password:
                    st.warning(
                        "Enter your email and password."
                    )
                else:
                    try:
                        result = api_request(
                            "POST",
                            "/auth/login",
                            json={
                                "email": email.strip(),
                                "password": password,
                            },
                        )

                        token = (
                            result.get("access_token")
                            if isinstance(result, dict)
                            else None
                        )

                        if not token:
                            st.error(
                                "The login response did not "
                                "contain an access token."
                            )
                        else:
                            st.session_state.token = token
                            st.session_state.email = email.strip()
                            notify("success", "Login successful!")
                            st.rerun()

                    except APIError as exc:
                        st.error(str(exc))

        with register_tab:
            st.subheader("Create your account")

            with st.form("register_form"):
                new_email = st.text_input(
                    "Email address",
                    placeholder="you@example.com",
                )
                new_password = st.text_input(
                    "Password",
                    type="password",
                )
                confirm_password = st.text_input(
                    "Confirm password",
                    type="password",
                )

                submitted = st.form_submit_button(
                    "Create account",
                    use_container_width=True,
                )

            if submitted:
                if not new_email.strip() or not new_password:
                    st.warning("Complete all required fields.")
                elif new_password != confirm_password:
                    st.error("The passwords do not match.")
                elif len(new_password) < 8:
                    st.error(
                        "Use a password with at least 8 characters."
                    )
                else:
                    try:
                        api_request(
                            "POST",
                            "/auth/register",
                            json={
                                "email": new_email.strip(),
                                "password": new_password,
                            },
                        )
                        st.success(
                            "Account created. You can now log in."
                        )
                    except APIError as exc:
                        st.error(str(exc))


# =========================================================
# DASHBOARD FILTERS
# =========================================================

def dashboard_filters(df):
    today = date.today()

    if not df.empty and df["expense_date"].notna().any():
        min_date = df["expense_date"].min().date()
        max_date = df["expense_date"].max().date()
    else:
        min_date = today.replace(day=1)
        max_date = today

    with st.container(border=True):
        st.markdown("### Filter your spending")

        col1, col2, col3 = st.columns([1, 1, 1.2])

        with col1:
            start_date = st.date_input(
                "Start date",
                value=min_date,
                key="dashboard_start_date",
            )

        with col2:
            end_date = st.date_input(
                "End date",
                value=max(max_date, min_date),
                key="dashboard_end_date",
            )

        with col3:
            categories = (
                sorted(df["category"].dropna().unique().tolist())
                if not df.empty
                else []
            )

            category = st.selectbox(
                "Category",
                ["All"] + categories,
                key="dashboard_category",
            )

    if start_date > end_date:
        st.error("Start date must be before or equal to end date.")
        return df.iloc[0:0].copy(), start_date, end_date, category

    filtered = filter_expenses(
        df, start_date, end_date, category
    )

    return filtered, start_date, end_date, category


# =========================================================
# ADVANCED DASHBOARD
# =========================================================

def dashboard_overview(df):
    st.subheader("Financial Overview")

    filtered, start_date, end_date, category = (
        dashboard_filters(df)
    )

    previous_start, previous_end = previous_period(
        start_date, end_date
    )

    previous_df = filter_expenses(
        df, previous_start, previous_end, category
    )

    current_total = period_total(filtered)
    previous_total = period_total(previous_df)

    current_count = len(filtered)
    previous_count = len(previous_df)

    average_expense = (
        current_total / current_count
        if current_count
        else 0
    )

    largest_expense = (
        float(filtered["amount"].max())
        if current_count
        else 0
    )

    total_delta = None
    count_delta = None

    if previous_total > 0:
        total_delta = (
            (current_total - previous_total)
            / previous_total
            * 100
        )

    if previous_count > 0:
        count_delta = (
            (current_count - previous_count)
            / previous_count
            * 100
        )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Spending",
        money(current_total),
        delta=(
            f"{total_delta:+.1f}% vs previous period"
            if total_delta is not None
            else None
        ),
        delta_color="inverse",
    )

    c2.metric(
        "Transactions",
        current_count,
        delta=(
            f"{count_delta:+.1f}% vs previous period"
            if count_delta is not None
            else None
        ),
        delta_color="off",
    )

    c3.metric(
        "Average Expense",
        money(average_expense),
    )

    c4.metric(
        "Largest Expense",
        money(largest_expense),
    )

    st.caption(
        f"Showing {start_date:%d %b %Y} – "
        f"{end_date:%d %b %Y}"
        + (
            f" · Category: {category}"
            if category != "All"
            else " · All categories"
        )
    )

    st.divider()

    if filtered.empty:
        st.info(
            "No expenses found for these filters. "
            "Try another date range or add an expense."
        )
        return

    # ---------------- Category analysis ----------------

    left, right = st.columns(2)

    with left:
        st.subheader("Spending by Category")

        category_totals = (
            filtered.groupby("category")["amount"]
            .sum()
            .sort_values(ascending=False)
        )

        st.bar_chart(
            category_totals,
            x_label="Category",
            y_label="Amount (₹)",
        )

    with right:
        st.subheader("Daily Spending Trend")

        daily = (
            filtered.assign(
                day=filtered["expense_date"].dt.strftime("%Y-%m-%d")
            )
            .groupby("day")["amount"]
            .sum()
            .sort_index()
        )

        st.line_chart(
            daily,
            x_label="Date",
            y_label="Amount (₹)",
        )

    # ---------------- Monthly trend ----------------

    st.divider()
    st.subheader("Monthly Spending Trend")

    monthly_source = filtered.copy()

    monthly_source["month"] = (
        monthly_source["expense_date"]
        .dt.to_period("M")
        .astype(str)
    )

    monthly_totals = (
        monthly_source.groupby("month")["amount"]
        .sum()
        .sort_index()
    )

    if len(monthly_totals) == 1:
        st.info(
            "Only one month of data is available in this "
            "filtered period. Expand the date range to compare "
            "multiple months."
        )

    st.bar_chart(
        monthly_totals,
        x_label="Month",
        y_label="Amount (₹)",
    )

    # ---------------- Category summary table ----------------

    st.divider()
    st.subheader("Category Summary")

    category_summary = (
        filtered.groupby("category")
        .agg(
            Transactions=("amount", "count"),
            Total=("amount", "sum"),
            Average=("amount", "mean"),
        )
        .sort_values("Total", ascending=False)
        .reset_index()
    )

    category_summary["Total"] = category_summary["Total"].map(money)
    category_summary["Average"] = category_summary["Average"].map(money)

    st.dataframe(
        category_summary,
        use_container_width=True,
        hide_index=True,
    )

    # ---------------- Recent expenses ----------------

    st.divider()
    st.subheader("Recent Transactions")

    recent = filtered.sort_values(
        "expense_date",
        ascending=False,
        na_position="last",
    ).head(10)

    st.dataframe(
        display_dataframe(recent),
        use_container_width=True,
        hide_index=True,
    )

    st.download_button(
        "Download Filtered Transactions (CSV)",
        data=display_dataframe(filtered).to_csv(
            index=False
        ).encode("utf-8"),
        file_name="spendwise_filtered_expenses.csv",
        mime="text/csv",
    )


# =========================================================
# MY EXPENSES
# =========================================================

def expenses_page(df):
    st.subheader("My Expenses")

    if df.empty:
        st.info("No expenses found. Add your first expense.")
        return

    category_options = (
        ["All"] + sorted(df["category"].dropna().unique().tolist())
    )

    col1, col2 = st.columns(2)

    with col1:
        search = st.text_input(
            "Search description or category",
            placeholder="Try food, travel, shopping...",
        )

    with col2:
        category = st.selectbox(
            "Filter category",
            category_options,
        )

    filtered = df.copy()

    if category != "All":
        filtered = filtered[filtered["category"] == category]

    if search.strip():
        term = search.strip().lower()

        filtered = filtered[
            filtered["description"].str.lower().str.contains(
                term, na=False
            )
            | filtered["category"].str.lower().str.contains(
                term, na=False
            )
        ]

    st.caption(f"{len(filtered)} transaction(s)")
    st.dataframe(
        display_dataframe(
            filtered.sort_values(
                "expense_date",
                ascending=False,
                na_position="last",
            )
        ),
        use_container_width=True,
        hide_index=True,
    )

    st.divider()
    st.subheader("Edit or Delete")

    if filtered.empty:
        st.info("No transactions match your search.")
        return

    records = filtered.to_dict("records")

    selected = st.selectbox(
        "Choose a transaction",
        records,
        format_func=lambda item: (
            f"#{item['id']} · {item['category']} · "
            f"{money(item['amount'])} · "
            f"{item['description'] or 'No description'}"
        ),
    )

    with st.form("edit_expense_form"):
        amount = st.number_input(
            "Amount (₹)",
            min_value=0.01,
            value=max(0.01, float(selected["amount"])),
            step=10.0,
        )

        edit_category = st.text_input(
            "Category",
            value=selected["category"],
        )

        description = st.text_input(
            "Description",
            value=selected["description"],
        )

        raw_date = selected["expense_date"]

        if pd.isna(raw_date):
            initial_date = date.today()
        else:
            initial_date = raw_date.date()

        expense_date = st.date_input(
            "Date",
            value=initial_date,
        )

        save = st.form_submit_button(
            "Save Changes",
            use_container_width=True,
        )

    if save:
        if not edit_category.strip():
            st.warning("Category cannot be empty.")
        else:
            payload = {
                "amount": amount,
                "category": edit_category.strip(),
                "description": description.strip(),
                "expense_date": expense_date.isoformat(),
            }

            try:
                api_request(
                    "PUT",
                    f"/expenses/{selected['id']}",
                    json=payload,
                )

                notify("success", "Expense updated.")
                st.rerun()

            except APIError as exc:
                st.error(str(exc))

    if st.button("Delete Selected Expense"):
        st.session_state.confirm_delete = selected["id"]

    if st.session_state.confirm_delete == selected["id"]:
        st.warning(
            "Confirm that you want to permanently delete this expense."
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Confirm Delete", type="primary"):
                try:
                    api_request(
                        "DELETE",
                        f"/expenses/{selected['id']}",
                    )

                    st.session_state.confirm_delete = None
                    notify("success", "Expense deleted.")
                    st.rerun()

                except APIError as exc:
                    st.error(str(exc))

        with col2:
            if st.button("Cancel"):
                st.session_state.confirm_delete = None
                st.rerun()


# =========================================================
# ADD EXPENSE
# =========================================================

def add_expense_page():
    st.subheader("Add Expense")
    st.write("Record a transaction to keep your spending up to date.")

    with st.form("add_expense_form", clear_on_submit=True):
        amount = st.number_input(
            "Amount (₹)",
            min_value=0.01,
            value=100.0,
            step=10.0,
        )

        category = st.selectbox(
            "Category",
            [
                "Food",
                "Transport",
                "Shopping",
                "Bills",
                "Health",
                "Education",
                "Entertainment",
                "Travel",
                "Other",
            ],
        )

        description = st.text_input(
            "Description",
            placeholder="Example: Lunch with friends",
        )

        expense_date = st.date_input(
            "Date",
            value=date.today(),
        )

        submitted = st.form_submit_button(
            "Save Expense",
            use_container_width=True,
        )

    if submitted:
        payload = {
            "amount": amount,
            "category": category,
            "description": description.strip(),
            "expense_date": expense_date.isoformat(),
        }

        try:
            api_request(
                "POST",
                "/expenses",
                json=payload,
            )

            notify("success", "Expense added successfully.")
            st.rerun()

        except APIError as exc:
            st.error(str(exc))


# =========================================================
# ANALYTICS PAGE
# =========================================================

def analytics_page(df):
    st.subheader("Advanced Analytics")

    if df.empty:
        st.info("Add expenses to see your analytics.")
        return

    valid = df.dropna(subset=["expense_date"]).copy()

    if valid.empty:
        st.info("No valid expense dates are available.")
        return

    min_date = valid["expense_date"].min().date()
    max_date = valid["expense_date"].max().date()

    start, end = st.date_input(
        "Analytics date range",
        value=(min_date, max_date),
        key="analytics_date_range",
    ) if False else (min_date, max_date)

    date_range = st.date_input(
        "Choose date range",
        value=(min_date, max_date),
        key="analytics_range",
    )

    if not isinstance(date_range, (tuple, list)) or len(date_range) != 2:
        st.info("Choose both a start date and an end date.")
        return

    start, end = date_range

    if start > end:
        st.error("Start date must not be after end date.")
        return

    filtered = filter_expenses(df, start, end)

    if filtered.empty:
        st.info("No transactions in this date range.")
        return

    total = period_total(filtered)
    count = len(filtered)
    average = total / count if count else 0

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Spending", money(total))
    c2.metric("Transactions", count)
    c3.metric("Average Transaction", money(average))

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Category Analysis")

        category_totals = (
            filtered.groupby("category")["amount"]
            .sum()
            .sort_values(ascending=False)
        )

        st.bar_chart(category_totals)

    with col2:
        st.markdown("### Monthly Analysis")

        filtered["month"] = (
            filtered["expense_date"]
            .dt.to_period("M")
            .astype(str)
        )

        monthly_totals = (
            filtered.groupby("month")["amount"]
            .sum()
            .sort_index()
        )

        st.line_chart(monthly_totals)

    st.divider()
    st.markdown("### Export Report")

    st.download_button(
        "Download Analytics Data",
        data=display_dataframe(filtered).to_csv(
            index=False
        ).encode("utf-8"),
        file_name="spendwise_analytics.csv",
        mime="text/csv",
    )


# =========================================================
# APPLICATION ENTRY POINT
# =========================================================

def main():
    if not st.session_state.token:
        authentication_page()
        return

    with st.sidebar:
        st.markdown("# 💰 SpendWise")
        st.caption("Personal Finance Dashboard")
        st.divider()

        st.write("Logged in as")
        st.write(st.session_state.email or "")

        page = st.radio(
            "Navigation",
            [
                "Dashboard",
                "My Expenses",
                "Add Expense",
                "Analytics",
            ],
        )

        st.divider()

        if st.button("Logout", use_container_width=True):
            st.session_state.token = None
            st.session_state.email = None
            st.session_state.confirm_delete = None
            notify("success", "Logged out successfully.")
            st.rerun()

    show_notice()

    st.markdown(
        '<p class="brand-title">SpendWise</p>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<p class="brand-subtitle">'
        'Your personal finance command center'
        '</p>',
        unsafe_allow_html=True,
    )

    try:
        with st.spinner("Loading your expenses..."):
            df = load_expenses()

    except APIError as exc:
        st.error(str(exc))
        st.info(
            "Verify that FastAPI is running and that the "
            "/expenses endpoint is available."
        )
        return

    if page == "Dashboard":
        dashboard_overview(df)

    elif page == "My Expenses":
        expenses_page(df)

    elif page == "Add Expense":
        add_expense_page()

    elif page == "Analytics":
        analytics_page(df)


if __name__ == "__main__":
    main()
