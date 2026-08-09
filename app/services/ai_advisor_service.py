"""
FinAI Pro
AI Financial Advisor Service

Analyzes a user's financial activity and generates
personalized financial guidance.
"""

from collections import defaultdict

from sqlalchemy.orm import Session

from app.models.income import Income
from app.models.expense import Expense


def get_financial_data(
    db: Session,
    user_id: int
):
    """
    Collects the user's financial information.
    """

    incomes = (
        db.query(Income)
        .filter(
            Income.user_id == user_id
        )
        .all()
    )

    expenses = (
        db.query(Expense)
        .filter(
            Expense.user_id == user_id
        )
        .all()
    )

    total_income = sum(
        income.amount
        for income in incomes
    )

    total_expenses = sum(
        expense.amount
        for expense in expenses
    )

    balance = (
        total_income
        - total_expenses
    )

    savings_rate = 0

    if total_income > 0:

        savings_rate = (
            balance / total_income
        ) * 100

    category_totals = defaultdict(float)

    for expense in expenses:

        category_totals[
            expense.category
        ] += expense.amount

    largest_category = None

    largest_category_amount = 0

    if category_totals:

        largest_category = max(
            category_totals,
            key=category_totals.get
        )

        largest_category_amount = (
            category_totals[
                largest_category
            ]
        )

    spending_ratio = 0

    if total_income > 0:

        spending_ratio = (
            total_expenses
            / total_income
        ) * 100

    return {

        "total_income": round(
            total_income,
            2
        ),

        "total_expenses": round(
            total_expenses,
            2
        ),

        "balance": round(
            balance,
            2
        ),

        "savings_rate": round(
            max(savings_rate, 0),
            1
        ),

        "spending_ratio": round(
            spending_ratio,
            1
        ),

        "largest_category":
            largest_category,

        "largest_category_amount":
            round(
                largest_category_amount,
                2
            ),

        "category_totals": {
            category: round(
                amount,
                2
            )
            for category, amount
            in category_totals.items()
        }

    }


def generate_financial_advice(
    financial_data: dict
):
    """
    Generates personalized financial advice
    based on the user's financial behavior.
    """

    income = financial_data[
        "total_income"
    ]

    expenses = financial_data[
        "total_expenses"
    ]

    balance = financial_data[
        "balance"
    ]

    savings_rate = financial_data[
        "savings_rate"
    ]

    spending_ratio = financial_data[
        "spending_ratio"
    ]

    largest_category = financial_data[
        "largest_category"
    ]

    largest_category_amount = financial_data[
        "largest_category_amount"
    ]


    recommendations = []

    warnings = []

    strengths = []


    if income <= 0:

        recommendations.append(
            "Add your income records so FinAI can provide a more accurate financial analysis."
        )

    else:

        if savings_rate >= 30:

            strengths.append(
                "Your current savings rate is strong."
            )

        elif savings_rate >= 15:

            strengths.append(
                "You are maintaining a moderate savings rate."
            )

        elif savings_rate > 0:

            recommendations.append(
                "Try to gradually increase your savings rate by reducing unnecessary spending."
            )

        else:

            warnings.append(
                "Your current expenses are using most or all of your income."
            )


        if spending_ratio > 90:

            warnings.append(
                "Your spending is very close to your total income."
            )

        elif spending_ratio > 75:

            recommendations.append(
                "Your spending level is relatively high compared with your income."
            )


    if largest_category:

        category_percentage = 0

        if expenses > 0:

            category_percentage = (
                largest_category_amount
                / expenses
            ) * 100


        if category_percentage >= 40:

            recommendations.append(
                f"{largest_category} is your largest expense category. Review this category for possible savings."
            )

        elif category_percentage >= 25:

            recommendations.append(
                f"{largest_category} represents a significant part of your spending. Keep an eye on this category."
            )


    if balance < 0:

        warnings.append(
            "Your total expenses are currently higher than your recorded income."
        )


    if not recommendations:

        recommendations.append(
            "Continue tracking your income and expenses regularly to maintain a clear view of your financial health."
        )


    if not strengths and balance > 0:

        strengths.append(
            "You currently have a positive financial balance."
        )


    if balance > 0:

        monthly_goal = balance * 0.20

    else:

        monthly_goal = 0


    return {

        "summary": create_summary(
            financial_data
        ),

        "recommendations":
            recommendations,

        "warnings":
            warnings,

        "strengths":
            strengths,

        "suggested_savings_goal":
            round(
                monthly_goal,
                2
            )

    }


def create_summary(
    financial_data: dict
):
    """
    Creates a simple human-readable
    financial summary.
    """

    income = financial_data[
        "total_income"
    ]

    expenses = financial_data[
        "total_expenses"
    ]

    balance = financial_data[
        "balance"
    ]

    savings_rate = financial_data[
        "savings_rate"
    ]


    if income <= 0:

        return (
            "There is not enough income data "
            "to provide a complete financial analysis."
        )


    if balance < 0:

        return (
            f"Your recorded expenses are higher "
            f"than your income. Your current "
            f"financial balance is negative and "
            f"your spending should be reviewed."
        )


    if savings_rate >= 30:

        return (
            f"Your financial position looks healthy. "
            f"You have a savings rate of "
            f"{savings_rate}% and a current balance "
            f"of ₹{balance:.2f}."
        )


    if savings_rate >= 15:

        return (
            f"Your finances are relatively stable. "
            f"Your current savings rate is "
            f"{savings_rate}%. There is room to "
            f"improve your savings."
        )


    return (
        f"Your current savings rate is "
        f"{savings_rate}%. Consider reducing "
        f"unnecessary expenses and increasing "
        f"the amount you save."
    )


def get_ai_financial_advice(
    db: Session,
    user_id: int
):
    """
    Main function used by the AI Advisor route.
    """

    financial_data = get_financial_data(
        db,
        user_id
    )

    advice = generate_financial_advice(
        financial_data
    )

    return {

        "financial_data":
            financial_data,

        "advice":
            advice

    }