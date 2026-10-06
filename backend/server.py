from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
import os
import db_connector

app = FastAPI()

current_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(current_dir, "..", "frontend", "templates")
templates = Jinja2Templates(directory=templates_dir)

# 🌟 জিনজা এনভায়রনমেন্টে রেঞ্জ এবং লেন্থ ফাংশন গ্লোবালি চিনিয়ে দেওয়া
templates.env.globals.update(range=range, len=len)


# ১. হোম রুট: পেজ খুললেই সরাসরি ১৪ তারিখের ডাটা সহ এড-আপডেট পেজে নিয়ে যাবে
@app.get("/", response_class=RedirectResponse)
async def read_root():
    return RedirectResponse(url="/ui/add-update?expense_date=2026-08-14")


# ২. মেইন ইন্টারফেস রুট (ডাটাবেজ থেকে ডাটা অটো-লোড মেকানিজম)
@app.get("/ui/add-update", response_class=HTMLResponse)
async def get_add_update_ui(request: Request, expense_date: str = "2026-08-14", rows: int = 0):
    try:
        parsed_date = datetime.strptime(expense_date, "%Y-%m-%d").date()
    except:
        parsed_date = datetime.strptime("2026-08-14", "%Y-%m-%d").date()
        expense_date = "2026-08-14"

    db_expenses = db_connector.fetch_data_by_date(parsed_date)
    total_rows_to_render = max(len(db_expenses) + rows, 1)

    return templates.TemplateResponse("add_update.html", {
        "request": request,
        "expenses": db_expenses,
        "selected_date": expense_date,
        "current_rows_count": rows,
        "total_rows_to_render": total_rows_to_render
    })


# ৩. ডাটা সেভ করার পিওর অফলাইন রুট
@app.post("/ui/save-expenses", response_class=HTMLResponse)
async def save_expenses_ui(
        request: Request,
        expense_date: str = Form(...),
        amount: list[float] = Form([]),
        category: list[str] = Form([]),
        notes: list[str] = Form([])
):
    parsed_date = datetime.strptime(expense_date, "%Y-%m-%d").date()
    db_connector.delete_expense(parsed_date)

    for i in range(len(amount)):
        if amount[i] is not None and category[i]:
            note_val = notes[i] if i < len(notes) else ""
            db_connector.insert_expense(parsed_date, amount[i], category[i], note_val)

    db_expenses = db_connector.fetch_data_by_date(parsed_date)

    return templates.TemplateResponse("add_update.html", {
        "request": request,
        "expenses": db_expenses,
        "selected_date": expense_date,
        "current_rows_count": 0,
        "total_rows_to_render": max(len(db_expenses), 1),
        "success_msg": "✅ Expenses saved successfully to the database!"
    })


# ৪. অ্যানালিটিক্স লজিক (বিশুদ্ধ অফলাইন চার্ট মেকার)
@app.get("/ui/analytics", response_class=HTMLResponse)
async def get_analytics_ui(request: Request, start_date: str = "2026-07-18", end_date: str = "2026-08-18"):
    try:
        parsed_start = datetime.strptime(start_date, "%Y-%m-%d").date()
        parsed_end = datetime.strptime(end_date, "%Y-%m-%d").date()
    except:
        parsed_start = datetime.strptime("2026-07-18", "%Y-%m-%d").date()
        parsed_end = datetime.strptime("2026-08-18", "%Y-%m-%d").date()

    data = db_connector.get_summary_by_date(parsed_start, parsed_end)
    total_period_spend = sum([row["total"] for row in data]) if data else 0

    processed_analytics = []
    if data:
        for row in data:
            percentage = (row["total"] * 100 / total_period_spend) if total_period_spend != 0 else 0
            processed_analytics.append({
                "category": row["category"],
                "total": row["total"],
                "percentage": round(percentage, 2)
            })

    return templates.TemplateResponse("analytics.html", {
        "request": request,
        "start_date": start_date,
        "end_date": end_date,
        "analytics_data": processed_analytics,
        "total_spend": total_period_spend
    })





