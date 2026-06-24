from flask import Flask, render_template_string, jsonify, request

app = Flask(__name__)

# Mock "προφίλ" για demo
PROFILES = [
    {
        "name": "Anna",
        "age": 27,
        "bio": "Λατρεύω τα ταξίδια, τον καφέ και τις βόλτες στη θάλασσα.",
        "image": "https://images.pexels.com/photos/415829/pexels-photo-415829.jpeg"
    },
    {
        "name": "Nikos",
        "age": 30,
        "bio": "Μου αρέσει η μουσική, το σινεμά και το καλό φαγητό.",
        "image": "https://images.pexels.com/photos/614810/pexels-photo-614810.jpeg"
    },
    {
        "name": "Eleni",
        "age": 25,
        "bio": "Bookworm, γυμναστήριο και βραδιές με φίλους.",
        "image": "https://images.pexels.com/photos/733872/pexels-photo-733872.jpeg"
    },
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="el">
<head>
    <meta charset="UTF-8">
    <title>Tzitzel</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }

        body {
            background: radial-gradient(circle at top, #ff6b81 0, #1b1b2f 55%, #000 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            color: #fff;
        }

        .app-container {
            width: 100%;
            max-width: 420px;
            height: 90vh;
            max-height: 780px;
            background: #111320;
            border-radius: 24px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.6);
            display: flex;
            flex-direction: column;
            overflow: hidden;
            position: relative;
        }

        .top-bar {
            height: 60px;
            padding: 0 16px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: rgba(0,0,0,0.35);
            backdrop-filter: blur(10px);
        }

        .top-bar-left, .top-bar-right {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .logo-circle {
            width: 34px;
            height: 34px;
            border-radius: 50%;
            background: linear-gradient(135deg, #ff6b81, #ff9f43);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            font-size: 18px;
        }

        .logo-text {
            font-weight: 700;
            letter-spacing: 1px;
            font-size: 18px;
        }

        .icon-btn {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            border: none;
            background: rgba(255,255,255,0.06);
            color: #fff;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-size: 16px;
        }

        .icon-btn:hover {
            background: rgba(255,255,255,0.15);
        }

        .content {
            flex: 1;
            padding: 16px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            position: relative;
        }

        .card {
            width: 100%;
            height: 70%;
            max-height: 520px;
            border-radius: 24px;
            overflow: hidden;
            position: relative;
            background: #000;
            box-shadow: 0 16px 30px rgba(0,0,0,0.7);
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
        }

        .card img {
            position: absolute;
            inset: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            filter: brightness(0.9);
        }

        .card-gradient {
            position: absolute;
            inset: 40% 0 0 0;
            background: linear-gradient(to top, rgba(0,0,0,0.9), transparent);
        }

        .card-info {
            position: relative;
            padding: 16px 18px 20px 18px;
            z-index: 2;
        }

        .name-row {
            display: flex;
            align-items: baseline;
            gap: 8px;
        }

        .name-row h2 {
            font-size: 24px;
            font-weight: 700;
        }

        .name-row span {
            font-size: 20px;
            opacity: 0.9;
        }

        .bio {
            margin-top: 6px;
            font-size: 14px;
            opacity: 0.9;
        }

        .chips {
            margin-top: 10px;
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
        }

        .chip {
            padding: 4px 10px;
            border-radius: 999px;
            font-size: 11px;
            background: rgba(255,255,255,0.12);
        }

        .buttons-row {
            margin-top: 18px;
            display: flex;
            justify-content: center;
            gap: 18px;
        }

        .round-btn {
            width: 64px;
            height: 64px;
            border-radius: 50%;
            border: none;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 26px;
            cursor: pointer;
            box-shadow: 0 10px 20px rgba(0,0,0,0.5);
            transition: transform 0.1s ease, box-shadow 0.1s ease;
        }

        .round-btn:active {
            transform: scale(0.94);
            box-shadow: 0 4px 10px rgba(0,0,0,0.6);
        }

        .btn-dislike {
            background: #fff;
            color: #ff4757;
        }

        .btn-like {
            background: #2ecc71;
            color: #fff;
        }

        .btn-superlike {
            background: #1e90ff;
            color: #fff;
        }

        .bottom-nav {
            height: 64px;
            display: flex;
            align-items: center;
            justify-content: space-around;
            background: rgba(0,0,0,0.6);
            backdrop-filter: blur(10px);
        }

        .nav-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            font-size: 11px;
            opacity: 0.7;
            cursor: pointer;
        }

        .nav-item span.icon {
            font-size: 18px;
            margin-bottom: 2px;
        }

        .nav-item.active {
            opacity: 1;
            color: #ff6b81;
        }

        .toast {
            position: absolute;
            top: 72px;
            left: 50%;
            transform: translateX(-50%);
            padding: 8px 14px;
            border-radius: 999px;
            background: rgba(0,0,0,0.8);
            font-size: 12px;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.25s ease;
        }

        .toast.show {
            opacity: 1;
        }

        @media (max-width: 480px) {
            .app-container {
                height: 100vh;
                max-height: none;
                border-radius: 0;
            }
        }
    </style>
</head>
<body>
<div class="app-container">
    <div class="top-bar">
        <div class="top-bar-left">
            <div class="logo-circle">T</div>
            <div class="logo-text">Tzitzel</div>
        </div>
        <div class="top-bar-right">
            <button class="icon-btn" title="Ρυθμίσεις">⚙</button>
            <button class="icon-btn" title="Μηνύματα">💬</button>
        </div>
    </div>

    <div class="content">
        <div id="toast" class="toast"></div>
        <div class="card" id="profile-card">
            <img id="profile-image" src="" alt="profile">
            <div class="card-gradient"></div>
            <div class="card-info">
                <div class="name-row">
                    <h2 id="profile-name">Όνομα</h2>
                    <span id="profile-age">0</span>
                </div>
                <p class="bio" id="profile-bio">Bio...</p>
                <div class="chips">
                    <div class="chip">Κοντά σου</div>
                    <div class="chip">Νέο μέλος</div>
                    <div class="chip">Tzitzel vibes ✨</div>
                </div>
                <div class="buttons-row">
                    <button class="round-btn btn-dislike" onclick="sendAction('dislike')" title="Dislike">✖</button>
                    <button class="round-btn btn-superlike" onclick="sendAction('superlike')" title="Super Like">★</button>
                    <button class="round-btn btn-like" onclick="sendAction('like')" title="Like">❤</button>
                </div>
            </div>
        </div>
    </div>
    
    <div class="card-info">
    <div class="name-row">
        <h2 id="profile-name">Όνομα</h2>
        <span id="profile-age">0</span>
    </div>
    <p class="bio" id="profile-bio">Bio...</p>
    <div class="chips">
        <div class="chip">Χόμπι σου</div>
        <div class="chip">Νέο μέλος</div>
        <div class="chip">Titzel vibes ✨</div>
    </div>
</div>

<div class="buttons">
    <button onclick="sendAction('like')">❤️ Like</button>
    <button onclick="sendAction('next')">➡️ Next</button>
</div>

    <div class="bottom-nav">
        <div class="nav-item active">
            <span class="icon">🔥</span>
            Ανακαλύψεις
        </div>
        <div class="nav-item">
            <span class="icon">💬</span>
            Μηνύματα
        </div>
        <div class="nav-item">
            <span class="icon">⭐</span>
            Premium
        </div>
        <div class="nav-item">
            <span class="icon">👤</span>
            Προφίλ
        </div>
    </div>
</div>

<script>
    let profiles = {{ profiles | tojson }};
    let currentIndex = 0;

    function showProfile(index) {
        if (profiles.length === 0) return;
        const p = profiles[index % profiles.length];
        document.getElementById("profile-name").textContent = p.name;
        document.getElementById("profile-age").textContent = p.age;
        document.getElementById("profile-bio").textContent = p.bio;
        document.getElementById("profile-image").src = p.image;
    }

    function showToast(text) {
        const toast = document.getElementById("toast");
        toast.textContent = text;
        toast.classList.add("show");
        setTimeout(() => toast.classList.remove("show"), 1200);
    }

    function sendAction(action) {
        fetch("/action", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({action: action, index: currentIndex})
        })
        .then(r => r.json())
        .then(data => {
            if (data.status === "ok") {
                if (action === "like") showToast("Έκανες like ✔");
                if (action === "dislike") showToast("Έκανες dislike ✖");
                if (action === "superlike") showToast("Super like! ★");
                currentIndex = (currentIndex + 1) % profiles.length;
                showProfile(currentIndex);
            }
        });
    }

    document.addEventListener("DOMContentLoaded", () => {
        showProfile(currentIndex);
    });
<script>
function sendAction(action) {
    fetch('/action', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: action })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Action sent:", data);
        location.reload();
    });
}

// Υπάρχει ήδη ο κώδικας σου εδώ για showProfile κ.λπ.
document.addEventListener("DOMContentLoaded", () => {
    showProfile(currentIndex);
});
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE, profiles=PROFILES)

@app.route("/action", methods=["POST"])
def action():
    data = request.get_json()
    action_type = data.get("action")
    index = data.get("index")
    # Εδώ θα μπορούσες να γράψεις σε DB, να κάνεις match κ.λπ.
    print(f"User action: {action_type} on profile index {index}")
    return jsonify({"status": "ok"})



if __name__ == '__main__':
    app.run()
    
