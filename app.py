from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)

# Data: Calories per unit (1 bowl, 1 piece, or 100g)
NUTRITION_DB = {
    "rice": {"cal": 130, "unit": "100g"},
    "roti": {"cal": 70, "unit": "piece"},
    "paneer": {"cal": 265, "unit": "100g"},
    "chicken": {"cal": 239, "unit": "100g"},
    "apple": {"cal": 52, "unit": "piece"},
    "egg": {"cal": 155, "unit": "piece"},
    "milk": {"cal": 42, "unit": "100ml"}
}

logs = []

@app.route('/', methods=['GET', 'POST'])
def home():
    total_today = 0
    if request.method == 'POST':
        item = request.form.get('item').lower().strip()
        qty = float(request.form.get('qty', 1))
        
        if item in NUTRITION_DB:
            unit_cal = NUTRITION_DB[item]['cal']
            calculated_cal = unit_cal * qty
            logs.append({
                'item': item.capitalize(), 
                'qty': qty, 
                'unit': NUTRITION_DB[item]['unit'], 
                'cal': calculated_cal
            })
        return redirect('/')
    
    for log in logs: total_today += log['cal']

    html_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            :root { --glass: rgba(255, 255, 255, 0.2); --grad: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
            body { background: var(--grad); min-height: 100vh; font-family: 'Poppins', sans-serif; color: white; padding: 20px; }
            .glass-card { background: var(--glass); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); border-radius: 20px; padding: 30px; }
            .form-control { background: rgba(255,255,255,0.1); border: none; color: white; }
            .form-control::placeholder { color: #ddd; }
            .btn-add { background: #00cec9; border: none; color: white; font-weight: bold; }
            .stat-circle { width: 150px; height: 150px; border: 8px solid #00cec9; border-radius: 50%; display: flex; flex-direction: column; justify-content: center; align-items: center; margin: 20px auto; }
        </style>
    </head>
    <body>
        <div class="container mt-5">
            <div class="row">
                <div class="col-md-5">
                    <div class="glass-card text-center">
                        <h3>Today's Goal</h3>
                        <div class="stat-circle">
                            <h2 class="mb-0">{{ total_today|int }}</h2>
                            <small>kcal</small>
                        </div>
                        <p>Keep going, Rachna!</p>
                    </div>
                </div>
                <div class="col-md-7">
                    <div class="glass-card">
                        <h4 class="mb-4">Log Your Meal</h4>
                        <form method="POST" class="row g-3">
                            <div class="col-8">
                                <input type="text" name="item" class="form-control" placeholder="Food (Rice, Roti, Egg...)" required>
                            </div>
                            <div class="col-4">
                                <input type="number" step="0.1" name="qty" class="form-control" placeholder="Qty" required>
                            </div>
                            <div class="col-12">
                                <button type="submit" class="btn btn-add w-100">Calculate & Add</button>
                            </div>
                        </form>
                        <hr>
                        <div class="mt-4">
                            {% for entry in logs %}
                            <div class="d-flex justify-content-between border-bottom py-2">
                                <span>{{ entry.item }} (x{{ entry.qty }})</span>
                                <strong>{{ entry.cal|int }} kcal</strong>
                            </div>
                            {% endfor %}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html_content, logs=logs, total_today=total_today)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)