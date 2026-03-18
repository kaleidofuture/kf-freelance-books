"""KF-FreelanceBooks — Freelance bookkeeping helper with keyword-based categorization."""

import io
from datetime import datetime, date

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="KF-FreelanceBooks",
    page_icon="📒",
    layout="wide",
)

from components.header import render_header
from components.footer import render_footer
from components.i18n import t

# --- Header ---
render_header()
st.info("💻 " + t("desktop_recommended"))

# --- Default Category Rules ---
DEFAULT_RULES_JA = [
    {"keyword": "交通", "category": "旅費交通費"},
    {"keyword": "タクシー", "category": "旅費交通費"},
    {"keyword": "Suica", "category": "旅費交通費"},
    {"keyword": "PASMO", "category": "旅費交通費"},
    {"keyword": "JR", "category": "旅費交通費"},
    {"keyword": "鉄道", "category": "旅費交通費"},
    {"keyword": "新幹線", "category": "旅費交通費"},
    {"keyword": "航空", "category": "旅費交通費"},
    {"keyword": "ANA", "category": "旅費交通費"},
    {"keyword": "JAL", "category": "旅費交通費"},
    {"keyword": "通信", "category": "通信費"},
    {"keyword": "電話", "category": "通信費"},
    {"keyword": "NTT", "category": "通信費"},
    {"keyword": "ソフトバンク", "category": "通信費"},
    {"keyword": "KDDI", "category": "通信費"},
    {"keyword": "au", "category": "通信費"},
    {"keyword": "docomo", "category": "通信費"},
    {"keyword": "インターネット", "category": "通信費"},
    {"keyword": "Wi-Fi", "category": "通信費"},
    {"keyword": "AWS", "category": "通信費"},
    {"keyword": "Google Cloud", "category": "通信費"},
    {"keyword": "Heroku", "category": "通信費"},
    {"keyword": "サーバ", "category": "通信費"},
    {"keyword": "ドメイン", "category": "通信費"},
    {"keyword": "Amazon", "category": "消耗品費"},
    {"keyword": "ヨドバシ", "category": "消耗品費"},
    {"keyword": "ビックカメラ", "category": "消耗品費"},
    {"keyword": "文具", "category": "消耗品費"},
    {"keyword": "事務用品", "category": "消耗品費"},
    {"keyword": "コンビニ", "category": "消耗品費"},
    {"keyword": "100均", "category": "消耗品費"},
    # Creator-specific rules
    {"keyword": "画材", "category": "消耗品費"},
    {"keyword": "CLIP STUDIO", "category": "消耗品費"},
    {"keyword": "Wacom", "category": "消耗品費"},
    {"keyword": "Adobe", "category": "消耗品費"},
    {"keyword": "フォント", "category": "消耗品費"},
    {"keyword": "素材", "category": "消耗品費"},
    {"keyword": "イラスト", "category": "新聞図書費"},
    {"keyword": "pixiv", "category": "新聞図書費"},
    {"keyword": "BOOTH", "category": "新聞図書費"},
    {"keyword": "電気", "category": "水道光熱費"},
    {"keyword": "ガス", "category": "水道光熱費"},
    {"keyword": "水道", "category": "水道光熱費"},
    {"keyword": "東京電力", "category": "水道光熱費"},
    {"keyword": "関西電力", "category": "水道光熱費"},
    {"keyword": "家賃", "category": "地代家賃"},
    {"keyword": "賃料", "category": "地代家賃"},
    {"keyword": "マンション", "category": "地代家賃"},
    {"keyword": "レンタルオフィス", "category": "地代家賃"},
    {"keyword": "コワーキング", "category": "地代家賃"},
    {"keyword": "WeWork", "category": "地代家賃"},
    {"keyword": "保険", "category": "保険料"},
    {"keyword": "飲食", "category": "接待交際費"},
    {"keyword": "会食", "category": "接待交際費"},
    {"keyword": "レストラン", "category": "接待交際費"},
    {"keyword": "居酒屋", "category": "接待交際費"},
    {"keyword": "カフェ", "category": "接待交際費"},
    {"keyword": "スタバ", "category": "接待交際費"},
    {"keyword": "Starbucks", "category": "接待交際費"},
    {"keyword": "書籍", "category": "新聞図書費"},
    {"keyword": "本", "category": "新聞図書費"},
    {"keyword": "Kindle", "category": "新聞図書費"},
    {"keyword": "新聞", "category": "新聞図書費"},
    {"keyword": "Udemy", "category": "研修費"},
    {"keyword": "セミナー", "category": "研修費"},
    {"keyword": "研修", "category": "研修費"},
    {"keyword": "外注", "category": "外注工賃"},
    {"keyword": "業務委託", "category": "外注工賃"},
    {"keyword": "報酬", "category": "売上"},
    {"keyword": "振込", "category": "売上"},
    {"keyword": "入金", "category": "売上"},
    {"keyword": "給与", "category": "売上"},
]

DEFAULT_RULES_EN = [
    {"keyword": "taxi", "category": "Transportation"},
    {"keyword": "uber", "category": "Transportation"},
    {"keyword": "lyft", "category": "Transportation"},
    {"keyword": "train", "category": "Transportation"},
    {"keyword": "airline", "category": "Transportation"},
    {"keyword": "flight", "category": "Transportation"},
    {"keyword": "phone", "category": "Communication"},
    {"keyword": "internet", "category": "Communication"},
    {"keyword": "mobile", "category": "Communication"},
    {"keyword": "AWS", "category": "Communication"},
    {"keyword": "hosting", "category": "Communication"},
    {"keyword": "domain", "category": "Communication"},
    {"keyword": "amazon", "category": "Supplies"},
    {"keyword": "office", "category": "Supplies"},
    {"keyword": "staples", "category": "Supplies"},
    # Creator-specific rules
    {"keyword": "art supplies", "category": "Supplies"},
    {"keyword": "CLIP STUDIO", "category": "Supplies"},
    {"keyword": "Wacom", "category": "Supplies"},
    {"keyword": "Adobe", "category": "Supplies"},
    {"keyword": "font", "category": "Supplies"},
    {"keyword": "illustration", "category": "Books & Education"},
    {"keyword": "pixiv", "category": "Books & Education"},
    {"keyword": "BOOTH", "category": "Books & Education"},
    {"keyword": "electric", "category": "Utilities"},
    {"keyword": "gas", "category": "Utilities"},
    {"keyword": "water", "category": "Utilities"},
    {"keyword": "rent", "category": "Rent"},
    {"keyword": "coworking", "category": "Rent"},
    {"keyword": "WeWork", "category": "Rent"},
    {"keyword": "insurance", "category": "Insurance"},
    {"keyword": "restaurant", "category": "Entertainment"},
    {"keyword": "dining", "category": "Entertainment"},
    {"keyword": "coffee", "category": "Entertainment"},
    {"keyword": "Starbucks", "category": "Entertainment"},
    {"keyword": "book", "category": "Books & Education"},
    {"keyword": "Kindle", "category": "Books & Education"},
    {"keyword": "Udemy", "category": "Books & Education"},
    {"keyword": "course", "category": "Books & Education"},
    {"keyword": "contractor", "category": "Subcontracting"},
    {"keyword": "freelance", "category": "Subcontracting"},
    {"keyword": "payment", "category": "Revenue"},
    {"keyword": "deposit", "category": "Revenue"},
    {"keyword": "invoice", "category": "Revenue"},
    {"keyword": "salary", "category": "Revenue"},
]


def get_default_rules() -> list[dict]:
    """Return default rules based on current language."""
    from components.i18n import get_lang

    if get_lang() == "ja":
        return DEFAULT_RULES_JA.copy()
    return DEFAULT_RULES_EN.copy()


def detect_columns(df: pd.DataFrame) -> dict:
    """Auto-detect date, amount, and description columns."""
    result = {"date": None, "amount": None, "description": None}

    for col in df.columns:
        col_lower = col.lower()
        # Date detection
        if result["date"] is None and any(
            kw in col_lower for kw in ["date", "日付", "日時", "年月日", "取引日"]
        ):
            result["date"] = col
        # Amount detection
        if result["amount"] is None and any(
            kw in col_lower
            for kw in [
                "amount",
                "金額",
                "出金",
                "支出",
                "入金",
                "取引金額",
                "お支払金額",
                "支払",
                "price",
            ]
        ):
            result["amount"] = col
        # Description detection
        if result["description"] is None and any(
            kw in col_lower
            for kw in ["description", "摘要", "適用", "内容", "取引内容", "明細", "memo", "備考", "お取引内容"]
        ):
            result["description"] = col

    # Fallback: use first string-like column for description
    if result["description"] is None:
        for col in df.columns:
            if df[col].dtype == object:
                result["description"] = col
                break

    return result


def classify_transaction(description: str, rules: list[dict], uncategorized_label: str) -> str:
    """Classify a transaction based on keyword matching."""
    if not isinstance(description, str):
        return uncategorized_label
    desc_lower = description.lower()
    for rule in rules:
        if rule["keyword"].lower() in desc_lower:
            return rule["category"]
    return uncategorized_label


def parse_amount(value) -> float:
    """Parse amount value, handling commas and yen signs."""
    if pd.isna(value):
        return 0.0
    s = str(value).replace(",", "").replace("¥", "").replace("\\", "").replace("$", "").replace(" ", "")
    # Handle negative amounts in parentheses: (1000) -> -1000
    if s.startswith("(") and s.endswith(")"):
        s = "-" + s[1:-1]
    try:
        return float(s)
    except ValueError:
        return 0.0


def get_tax_recommendation(annual_income: float) -> tuple[str, str]:
    """Return (recommendation_key, detail) based on annual income."""
    from components.i18n import get_lang

    if annual_income <= 300:
        return "tax_rec_white", "tax_rec_white_detail"
    elif annual_income <= 1000:
        return "tax_rec_simple_blue", "tax_rec_simple_blue_detail"
    else:
        return "tax_rec_full_blue", "tax_rec_full_blue_detail"


# --- Sidebar: Tax Filing Guide ---
with st.sidebar:
    st.markdown(f"### {t('tax_guide_title')}")
    st.caption(t("tax_guide_help"))
    annual_income = st.number_input(
        t("tax_guide_income_label"),
        min_value=0.0,
        max_value=100000.0,
        value=0.0,
        step=50.0,
        format="%.0f",
    )
    if annual_income > 0:
        rec_key, detail_key = get_tax_recommendation(annual_income)
        st.success(t(rec_key))
        st.caption(t(detail_key))

# --- Main UI ---

# Step 1: Upload CSV
st.markdown(f"### {t('step1_upload')}")
uploaded_file = st.file_uploader(t("upload_prompt"), type=["csv"])

if uploaded_file is not None:
    try:
        raw = uploaded_file.getvalue()
        # Try utf-8-sig first (common for Japanese bank CSVs), then shift_jis
        for enc in ["utf-8-sig", "utf-8", "shift_jis", "cp932"]:
            try:
                df = pd.read_csv(io.BytesIO(raw), encoding=enc)
                break
            except (UnicodeDecodeError, pd.errors.ParserError):
                continue
        else:
            df = pd.read_csv(io.BytesIO(raw), encoding="utf-8", errors="replace")

        st.success(t("file_loaded").format(rows=len(df), cols=len(df.columns)))

        # Preview
        with st.expander(t("data_preview"), expanded=True):
            st.dataframe(df.head(20), use_container_width=True)

        # Step 2: Column mapping
        st.markdown(f"### {t('step2_mapping')}")
        detected = detect_columns(df)

        col1, col2, col3 = st.columns(3)
        with col1:
            date_col = st.selectbox(
                t("col_date"),
                options=[""] + df.columns.tolist(),
                index=(df.columns.tolist().index(detected["date"]) + 1)
                if detected["date"]
                else 0,
            )
        with col2:
            amount_col = st.selectbox(
                t("col_amount"),
                options=[""] + df.columns.tolist(),
                index=(df.columns.tolist().index(detected["amount"]) + 1)
                if detected["amount"]
                else 0,
            )
        with col3:
            desc_col = st.selectbox(
                t("col_description"),
                options=[""] + df.columns.tolist(),
                index=(df.columns.tolist().index(detected["description"]) + 1)
                if detected["description"]
                else 0,
            )

        if not amount_col or not desc_col:
            st.warning(t("mapping_required"))
        else:
            # Step 3: Category rules
            st.markdown(f"### {t('step3_rules')}")
            st.caption(t("rules_description"))

            if "rules" not in st.session_state:
                st.session_state["rules"] = get_default_rules()

            rules_df = pd.DataFrame(st.session_state["rules"])
            edited_rules = st.data_editor(
                rules_df,
                num_rows="dynamic",
                use_container_width=True,
                column_config={
                    "keyword": st.column_config.TextColumn(t("rule_keyword")),
                    "category": st.column_config.TextColumn(t("rule_category")),
                },
            )

            # Update rules from editor
            current_rules = edited_rules.to_dict("records")
            current_rules = [r for r in current_rules if r.get("keyword") and r.get("category")]

            # Step 4: Classify
            st.markdown(f"### {t('step4_classify')}")

            if st.button(t("run_classify"), type="primary"):
                uncategorized = t("uncategorized")

                # Build working dataframe
                work_df = pd.DataFrame()
                if date_col:
                    work_df[t("col_date")] = df[date_col].astype(str)
                work_df[t("col_description")] = df[desc_col].astype(str)
                work_df[t("col_amount")] = df[amount_col].apply(parse_amount)
                work_df[t("col_category")] = df[desc_col].apply(
                    lambda x: classify_transaction(x, current_rules, uncategorized)
                )

                st.session_state["classified_df"] = work_df
                st.session_state["uncategorized_label"] = uncategorized

            if "classified_df" in st.session_state:
                work_df = st.session_state["classified_df"]
                uncategorized = st.session_state["uncategorized_label"]

                # Show classified transactions
                st.dataframe(work_df, use_container_width=True)

                # --- Manual Entry Section ---
                st.markdown(f"#### {t('manual_entry_title')}")
                with st.expander(t("manual_entry_expand")):
                    with st.form("manual_entry_form"):
                        me_col1, me_col2 = st.columns(2)
                        with me_col1:
                            me_date = st.date_input(t("manual_date"), value=date.today())
                            me_desc = st.text_input(t("manual_description"))
                        with me_col2:
                            me_amount = st.number_input(
                                t("manual_amount"),
                                value=0.0,
                                step=100.0,
                                format="%.0f",
                                help=t("manual_amount_help"),
                            )
                            # Gather unique categories from current rules
                            all_categories = sorted(set(r["category"] for r in current_rules)) if current_rules else [t("uncategorized")]
                            me_category = st.selectbox(t("manual_category"), options=all_categories)

                        me_submitted = st.form_submit_button(t("manual_add"), type="secondary")

                    if me_submitted and me_desc:
                        new_row = {
                            t("col_date"): me_date.strftime("%Y-%m-%d") if t("col_date") in work_df.columns else None,
                            t("col_description"): me_desc,
                            t("col_amount"): me_amount,
                            t("col_category"): me_category,
                        }
                        # Remove None columns
                        new_row = {k: v for k, v in new_row.items() if v is not None}
                        new_row_df = pd.DataFrame([new_row])
                        st.session_state["classified_df"] = pd.concat(
                            [work_df, new_row_df], ignore_index=True
                        )
                        st.rerun()

                # Stats
                cat_col = t("col_category")
                amt_col = t("col_amount")

                # Separate income and expenses
                expenses = work_df[work_df[amt_col] < 0].copy()
                income = work_df[work_df[amt_col] > 0].copy()

                # Category summary (expenses)
                st.markdown(f"### {t('step5_summary')}")

                if not expenses.empty:
                    st.markdown(f"#### {t('expense_summary')}")
                    expense_summary = (
                        expenses.groupby(cat_col)[amt_col]
                        .agg(["sum", "count"])
                        .rename(columns={"sum": t("total_amount"), "count": t("transaction_count")})
                        .sort_values(t("total_amount"))
                    )
                    expense_summary[t("total_amount")] = expense_summary[t("total_amount")].abs()
                    st.dataframe(expense_summary, use_container_width=True)

                    total_expense = expenses[amt_col].sum()
                    st.metric(t("total_expenses"), f"¥{abs(total_expense):,.0f}")

                if not income.empty:
                    st.markdown(f"#### {t('income_summary')}")
                    income_summary = (
                        income.groupby(cat_col)[amt_col]
                        .agg(["sum", "count"])
                        .rename(columns={"sum": t("total_amount"), "count": t("transaction_count")})
                        .sort_values(t("total_amount"), ascending=False)
                    )
                    st.dataframe(income_summary, use_container_width=True)

                    total_income = income[amt_col].sum()
                    st.metric(t("total_income"), f"¥{total_income:,.0f}")

                # Uncategorized count
                uncat_count = len(work_df[work_df[cat_col] == uncategorized])
                if uncat_count > 0:
                    st.warning(t("uncategorized_warning").format(count=uncat_count))

                # Step 6: Download
                st.markdown(f"### {t('step6_download')}")

                # Full classified CSV
                csv_full = work_df.to_csv(index=False).encode("utf-8-sig")
                st.download_button(
                    label=t("download_classified"),
                    data=csv_full,
                    file_name="classified_transactions.csv",
                    mime="text/csv",
                )

                # Category summary CSV (for tax filing)
                if not expenses.empty:
                    summary_for_tax = (
                        expenses.groupby(cat_col)[amt_col]
                        .sum()
                        .abs()
                        .reset_index()
                        .rename(columns={cat_col: t("tax_category_col"), amt_col: t("tax_amount_col")})
                        .sort_values(t("tax_amount_col"), ascending=False)
                    )
                    csv_summary = summary_for_tax.to_csv(index=False).encode("utf-8-sig")
                    st.download_button(
                        label=t("download_summary"),
                        data=csv_summary,
                        file_name="expense_summary_by_category.csv",
                        mime="text/csv",
                    )

    except Exception as e:
        st.error(f"{t('load_error')}: {e}")

else:
    st.info(t("no_file"))

# --- Footer ---
render_footer(libraries=["pandas"], repo_name="kf-freelance-books")
