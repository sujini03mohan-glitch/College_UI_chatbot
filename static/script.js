function scrollToCourses() {
    document.getElementById("courses").scrollIntoView({
        behavior: "smooth"
    });
}

function toggleChat() {
    let chat = document.getElementById("chatbox");
    chat.style.display = (chat.style.display === "flex") ? "none" : "flex";
}
function openForm(courseName) {
    document.getElementById("formModal").style.display = "block";
    document.getElementById("course").value = courseName;
}

function closeForm() {
    document.getElementById("formModal").style.display = "none";
}

async function submitForm() {
    let data = {
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        phone: document.getElementById("phone").value,
        course: document.getElementById("course").value
    };

    let response = await fetch("/send-email", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    let result = await response.json();
    alert(result.message);

    closeForm();
}

async function sendMessage() {
    let input = document.getElementById("userInput");
    let message = input.value;

    let messages = document.getElementById("messages");

    // USER MESSAGE
    messages.innerHTML += 
        `<div class="message user">${message}</div>`;

    // SCROLL DOWN
    messages.scrollTop = messages.scrollHeight;

    let response = await fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message })
    });

    let data = await response.json();

    // BOT MESSAGE
    messages.innerHTML += 
        `<div class="message bot">${data.response}</div>`;

    messages.scrollTop = messages.scrollHeight;
     

    input.value = "";
}
// SPEECH RECOGNITION
function startVoice() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();

    recognition.lang = "en-US";
    recognition.start();

    recognition.onresult = function(event) {
        let voiceText = event.results[0][0].transcript;
        document.getElementById("userInput").value = voiceText;
        sendMessage(); // auto send
    };

    recognition.onerror = function() {
        alert("Voice recognition not supported in your browser");
    };
}

// TEXT TO SPEECH

var swiper = new Swiper(".bgSwiper", {
    loop: true,
    autoplay: {
        delay: 3000,
    },
    effect: "fade",
});

// AUTO OPEN CHAT AFTER 3 SECONDS
window.onload = function () {
    setTimeout(() => {
        let chat = document.getElementById("chatbox");
        chat.style.display = "flex";
    }, 3000);
};
