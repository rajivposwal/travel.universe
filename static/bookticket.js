/* === bookticket.js — ASRS Travel v3.0 === */

document.addEventListener('DOMContentLoaded', () => {

    /* ─── Theme Manager ───────────────────────── */
    const root = document.documentElement;
    const btn = document.getElementById('theme-toggle');
    const icon = btn?.querySelector('i');

    const applyTheme = (t) => {
        root.setAttribute('data-theme', t);
        localStorage.setItem('kyt-theme', t);
        if (icon) icon.className = t === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    };
    applyTheme(localStorage.getItem('kyt-theme') || 'light');
    btn?.addEventListener('click', () => {
        applyTheme(root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
    });

    /* ─── Tab Switcher ────────────────────────── */
    document.querySelectorAll('.cat-tab').forEach(tab => {
        tab.addEventListener('click', () => {
            const target = tab.dataset.target;
            document.querySelectorAll('.cat-tab').forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            document.querySelectorAll('.tab-pane').forEach(pane => {
                pane.id === `${target}-pane` ? pane.classList.remove('hidden') : pane.classList.add('hidden');
            });
        });
    });

    /* ─── Star Rating ────────────────────────── */
    const stars = document.querySelectorAll('.stars i');
    const rMsg = document.querySelector('.rating-msg');
    const labels = ['', 'Terrible', 'Poor', 'Okay', 'Good', 'Excellent!'];
    let chosen = 0;

    stars.forEach((s, i) => {
        s.addEventListener('mouseenter', () => stars.forEach((x, j) => x.classList.toggle('lit', j <= i)));
        s.addEventListener('mouseleave', () => stars.forEach((x, j) => x.classList.toggle('lit', j < chosen)));
        s.addEventListener('click', () => {
            chosen = i + 1;
            if (rMsg) rMsg.textContent = `${labels[chosen]} ─ Thanks for your feedback!`;
        });
    });

    /* ─── Geo Locate ─────────────────────────── */
    window.locateCity = async (inputId) => {
        const input = document.getElementById(inputId);
        if (!input || !navigator.geolocation) return;
        const icon = input.parentElement?.querySelector('.locate-icon');
        icon?.classList.add('fa-spin');
        navigator.geolocation.getCurrentPosition(async pos => {
            try {
                const res = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${pos.coords.latitude}&lon=${pos.coords.longitude}`);
                const data = await res.json();
                input.value = data.address.city || data.address.town || data.address.state_district || 'Delhi';
            } catch { }
            icon?.classList.remove('fa-spin');
        }, () => icon?.classList.remove('fa-spin'));
    };

    /* ─── Voice Assistant Accessibility ─── */
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
        // Inject button and toast
        document.body.insertAdjacentHTML('beforeend', `
            <button class="voice-btn" id="voice-assistant-btn" title="Voice Assistant (Shift+Space)" aria-label="Activate Voice Assistant">
                <i class="fas fa-microphone"></i>
            </button>
            <div class="voice-status-toast" id="voice-toast">Voice Assistant enabled</div>
        `);

        const vBtn = document.getElementById('voice-assistant-btn');
        const vToast = document.getElementById('voice-toast');
        const recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.lang = 'en-US';

        const speak = (text) => {
            const synth = window.speechSynthesis;
            synth.cancel(); // clear queue
            const uttr = new SpeechSynthesisUtterance(text);
            uttr.rate = 0.95;
            uttr.pitch = 1.0;
            synth.speak(uttr);
        };

        const showToast = (msg) => {
            vToast.textContent = msg;
            vToast.classList.add('visible');
            setTimeout(() => vToast.classList.remove('visible'), 3000);
        };

        const processCommand = (cmd) => {
            cmd = cmd.toLowerCase().trim();
            showToast(`Heard: "${cmd}"`);

            if (cmd.includes('home') || cmd.includes('start page') || cmd.includes('go back')) {
                speak('Navigating to the home page.');
                setTimeout(() => window.location.href = '/', 1500);
            }
            else if (cmd.includes('profile') || cmd.includes('my account') || cmd.includes('dashboard')) {
                speak('Opening your profile and booking dashboard.');
                setTimeout(() => window.location.href = '/profile', 1500);
            }
            else if (cmd.includes('deal') || cmd.includes('offers') || cmd.includes('discount')) {
                speak('Showing you the best travel deals right now.');
                setTimeout(() => window.location.href = '/deals', 1500);
            }
            else if (cmd.includes('hotel') || cmd.includes('room') || cmd.includes('stay')) {
                speak('Opening our curated list of budget hotels.');
                setTimeout(() => window.location.href = '/hotels', 1500);
            }
            else if (cmd.includes('logout') || cmd.includes('sign out') || cmd.includes('log out')) {
                speak('Logging you out safely. Goodbye!');
                setTimeout(() => window.location.href = '/logout', 1500);
            }
            else if (cmd.includes('search') || cmd.includes('find')) {
                speak('Initiating your search.');
                const form = document.querySelector('form.search-grid') || document.querySelector('form');
                if (form) form.submit();
                else speak('I could not find a search form on this page.');
            }
            else if (cmd.includes('book') || cmd.includes('pay') || cmd.includes('confirm')) {
                // If on booking page and buttons exist
                speak('Attempting to proceed with booking.');
                const btn1 = document.getElementById('btn-next-1');
                const btnPay = document.querySelector('.pay-btn');
                if (btnPay) btnPay.click();
                else if (btn1) btn1.click();
                else document.querySelector('.btn-primary')?.click();
            }
            else if (cmd.startsWith('type') || cmd.startsWith('enter') || cmd.startsWith('write')) {
                // e.g., "type john doe in name" or "enter delhi in origin"
                const parts = cmd.split(' in ');
                if (parts.length > 1) {
                    const val = parts[0].replace('type ', '').replace('enter ', '').replace('write ', '').trim();
                    const target = parts[1].trim();
                    const inputs = document.querySelectorAll('input');
                    let found = false;
                    for (let input of inputs) {
                        if ((input.name && input.name.toLowerCase().includes(target)) ||
                            (input.placeholder && input.placeholder.toLowerCase().includes(target)) ||
                            (input.id && input.id.toLowerCase().includes(target))) {
                            input.value = val;
                            speak(`Entered ${val} into ${target}`);
                            found = true;
                            break;
                        }
                    }
                    if (!found) speak(`Could not find an input field matching ${target}`);
                } else {
                    speak("Please specify where to type it. For example: type Delhi in origin.");
                }
            }
            else if (cmd.includes('scroll down')) {
                speak('Scrolling down.');
                window.scrollBy({ top: 500, behavior: 'smooth' });
            }
            else if (cmd.includes('scroll up')) {
                speak('Scrolling up.');
                window.scrollBy({ top: -500, behavior: 'smooth' });
            }
            else if (cmd.startsWith('click')) {
                // e.g "click search" or "click next"
                const btnName = cmd.replace('click', '').trim();
                const buttons = document.querySelectorAll('button, a, .btn');
                let found = false;
                for (let btn of buttons) {
                    if (btn.innerText.toLowerCase().includes(btnName) || (btn.title && btn.title.toLowerCase().includes(btnName))) {
                        speak(`Clicking ${btnName}`);
                        btn.click();
                        found = true;
                        break;
                    }
                }
                if (!found) speak(`I could not find a button named ${btnName}`);
            }
            else {
                speak('I heard you, but I do not have a specific action for that. Try saying: go to deals, type [text] in [field], click [button], scroll down, or logout.');
            }
        };

        vBtn.addEventListener('click', () => {
            if (vBtn.classList.contains('listening')) {
                recognition.stop();
                vBtn.classList.remove('listening');
                speak('Voice assistant deactivated.');
            } else {
                vBtn.classList.add('listening');
                showToast('Listening... Please speak now.');
                try {
                    recognition.start();
                } catch (e) {
                    console.error("Mic start err:", e);
                    vBtn.classList.remove('listening');
                }
            }
        });

        // Add keyboard shortcut (Shift + Space) for accessibility without mouse
        document.addEventListener('keydown', (e) => {
            if (e.shiftKey && e.code === 'Space') {
                e.preventDefault();
                vBtn.click();
            }
        });

        recognition.onresult = (e) => {
            const transcript = e.results[0][0].transcript;
            vBtn.classList.remove('listening');
            processCommand(transcript);
        };

        recognition.onend = () => {
            vBtn.classList.remove('listening');
        };

        recognition.onerror = (event) => {
            console.error("Speech Error:", event.error);
            if (event.error === 'not-allowed') {
                speak('Microphone access is blocked. Please allow permissions in your browser.');
            } else if (event.error !== 'no-speech') {
                speak('There was an issue capturing your voice. Please try again.');
            }
            vBtn.classList.remove('listening');
        };
    }

});
