const log = document.getElementById("log");
const form = document.getElementById("form");
const input = document.getElementById("q");
const sendBtn = document.getElementById("sendBtn");

function addMessage(text, cls, metaInfo = null) {
  const d = document.createElement("div");
  d.className = "msg " + cls;
  d.textContent = text;

  if (metaInfo) {
    const m = document.createElement("div");
    m.className = "meta";

    const tag = document.createElement("span");
    tag.className = "tag";
    tag.textContent = metaInfo.status === "unavailable" ? "Not in campus data" : "Presidency Grounded";
    m.append(tag);

    const srcSpan = document.createElement("span");
    srcSpan.textContent = (metaInfo.sources?.length ? metaInfo.sources.map(s => s.label || s).join(", ") : "No source matched") + " · " + (metaInfo.model || "Presidency AI Engine");
    m.append(srcSpan);

    d.append(m);
  }

  log.append(d);
  log.scrollTop = log.scrollHeight;
  return d;
}

async function ask(query) {
  query = query.trim();
  if (!query) return;

  addMessage(query, "user");
  const waitBubble = addMessage("Consulting Presidency University knowledge base…", "bot");
  if (sendBtn) sendBtn.disabled = true;

  const groq = document.getElementById("groqKey")?.value?.trim() || "";
  const gemini = document.getElementById("geminiKey")?.value?.trim() || "";
  const openai = document.getElementById("openaiKey")?.value?.trim() || "";

  try {
    const r = await fetch("/api/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query, groqKey: groq, geminiKey: gemini, openaiKey: openai })
    });
    const data = await r.json();
    waitBubble.remove();
    if (data.ok) {
      addMessage(data.answer, "bot" + (data.status === "unavailable" ? " unavailable" : ""), data);
    } else {
      addMessage(data.error || "Unable to answer question.", "bot unavailable");
    }
  } catch (err) {
    waitBubble.remove();
    addMessage("Could not reach backend server. Please verify app.py is running.", "bot unavailable");
  } finally {
    if (sendBtn) sendBtn.disabled = false;
    input.focus();
  }
}

if (form) {
  form.addEventListener("submit", e => {
    e.preventDefault();
    const q = input.value.trim();
    if (q) {
      input.value = "";
      ask(q);
    }
  });
}

// Load catalog topics from /api/catalog
fetch("/api/catalog").then(r => r.json()).then(({ domains }) => {
  const topicsUl = document.getElementById("topics");
  if (!topicsUl) return;
  topicsUl.innerHTML = "";
  domains.forEach(item => {
    const li = document.createElement("li");
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "topic-btn";
    btn.innerHTML = `<span class="icon">${item.icon || '◈'}</span> <span>${item.label}</span>`;
    btn.title = item.summary;
    btn.onclick = () => ask(`Tell me about ${item.label.toLowerCase()} at Presidency University`);
    li.append(btn);
    topicsUl.append(li);
  });
}).catch(() => {});

// Quick Chips
document.querySelectorAll(".chip").forEach(chip => {
  chip.addEventListener("click", () => {
    const q = chip.getAttribute("data-q");
    if (q) ask(q);
  });
});

// Theme Toggle
const themeBtn = document.getElementById("themeToggle");
if (themeBtn) {
  themeBtn.addEventListener("click", () => {
    const current = document.documentElement.getAttribute("data-theme");
    const next = current === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", next);
    localStorage.setItem("pu_theme", next);
  });
  const savedTheme = localStorage.getItem("pu_theme");
  if (savedTheme) document.documentElement.setAttribute("data-theme", savedTheme);
}

// Clear Chat
const clearBtn = document.getElementById("clearBtn");
if (clearBtn) {
  clearBtn.addEventListener("click", () => {
    if (confirm("Clear consultation history?")) {
      const messages = log.querySelectorAll(".msg");
      messages.forEach(m => m.remove());
    }
  });
}

// Voice Input
const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
if (SpeechRec) {
  const micBtn = document.getElementById("mic");
  if (micBtn) {
    micBtn.hidden = false;
    micBtn.addEventListener("click", () => {
      try {
        const rec = new SpeechRec();
        rec.lang = "en-IN";
        micBtn.style.color = "#ef4444";
        rec.onresult = (e) => {
          input.value = e.results[0][0].transcript;
          input.focus();
        };
        rec.onend = () => { micBtn.style.color = ""; };
        rec.onerror = () => { micBtn.style.color = ""; };
        rec.start();
      } catch (e) {
        micBtn.style.color = "";
      }
    });
  }
}
