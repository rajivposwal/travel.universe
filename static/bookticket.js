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

});
