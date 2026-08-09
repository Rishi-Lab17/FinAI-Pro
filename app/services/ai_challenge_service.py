"""
FinAI Pro
AI Challenge Mode Service

Generates personalized financial challenges based
on the user's actual income and spending behavior.
"""

from collections import defaultdict

from sqlalchemy.orm import Session

from app.models.income import Income
from app.models.expense import Expense


# =========================================================
# USER FINANCIAL PROFILE
# =========================================================

def get_user_financial_profile(
    db: Session,
    user_id: int
):
    """
    Builds a financial profile from the user's
    recorded income and expenses.
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
        float(item.amount or 0)
        for item in incomes
    )

    total_expenses = sum(
        float(item.amount or 0)
        for item in expenses
    )

    balance = (
        total_income -
        total_expenses
    )

    savings_rate = 0

    if total_income > 0:

        savings_rate = (
            balance /
            total_income
        ) * 100

    category_totals = defaultdict(float)

    for expense in expenses:

        category = (
            expense.category
            or "Other"
        )

        category_totals[
            category
        ] += float(
            expense.amount or 0
        )

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

    return {

        "total_income":
            round(
                total_income,
                2
            ),

        "total_expenses":
            round(
                total_expenses,
                2
            ),

        "balance":
            round(
                balance,
                2
            ),

        "savings_rate":
            round(
                savings_rate,
                1
            ),

        "largest_category":
            largest_category,

        "largest_category_amount":
            round(
                largest_category_amount,
                2
            )
    }


# =========================================================
# GENERATE CHALLENGES
# =========================================================

def generate_challenges(
    profile: dict
):
    """
    Generates personalized financial challenges.
    """

    challenges = []

    savings_rate = profile[
        "savings_rate"
    ]

    total_expenses = profile[
        "total_expenses"
    ]

    balance = profile[
        "balance"
    ]

    largest_category = profile[
        "largest_category"
    ]

    largest_category_amount = profile[
        "largest_category_amount"
    ]


    # =====================================================
    # BALANCE RECOVERY
    # =====================================================

    if balance < 0:

        challenges.append({

            "title":
                "Balance Recovery Challenge",

            "description":
                "Reduce your spending and bring your balance back into positive territory.",

            "target":
                "Spend less than your recorded income.",

            "difficulty":
                "High"
        })


    # =====================================================
    # SAVINGS CHALLENGE
    # =====================================================

    if savings_rate < 10:

        challenges.append({

            "title":
                "Start Saving Challenge",

            "description":
                "Try to save at least 10 percent of your income.",

            "target":
                "Reach a 10 percent savings rate.",

            "difficulty":
                "Medium"
        })

    elif savings_rate < 20:

        challenges.append({

            "title":
                "20 Percent Savings Challenge",

            "description":
                "Increase your savings rate toward 20 percent.",

            "target":
                "Save 20 percent of your income.",

            "difficulty":
                "Medium"
        })

    else:

        challenges.append({

            "title":
                "Savings Booster Challenge",

            "description":
                "Push your savings rate slightly higher than your current level.",

            "target":
                "Increase your current savings rate by 5 percent.",

            "difficulty":
                "Medium"
        })


    # =====================================================
    # LARGEST EXPENSE CATEGORY
    # =====================================================

    if largest_category:

        reduction_target = (
            largest_category_amount *
            0.10
        )

        challenges.append({

            "title":
                f"{largest_category} Reduction Challenge",

            "description":
                f"Try reducing your {largest_category.lower()} spending.",

            "target":
                f"Save at least ₹{reduction_target:.2f} from this category.",

            "difficulty":
                "Medium"
        })


    # =====================================================
    # EXPENSE TRACKING
    # =====================================================

    if total_expenses > 0:

        challenges.append({

            "title":
                "Expense Tracking Challenge",

            "description":
                "Record every expense consistently so FinAI can identify your spending patterns more accurately.",

            "target":
                "Record all expenses for the next 7 days.",

            "difficulty":
                "Easy"
        })


    # =====================================================
    # FALLBACK
    # =====================================================

    if not challenges:

        challenges.append({

            "title":
                "Financial Awareness Challenge",

            "description":
                "Continue recording your income and expenses regularly.",

            "target":
                "Maintain consistent financial tracking.",

            "difficulty":
                "Easy"
        })


    return challenges


# =========================================================
# MAIN FUNCTION
# =========================================================

def get_ai_challenges(
    db: Session,
    user_id: int
):
    """
    Main function used by the AI Challenge route.
    """

    profile = get_user_financial_profile(
        db,
        user_id
    )

    challenges = generate_challenges(
        profile
    )

    return {

        "profile":
            profile,

        "challenges":
            challenges
    }