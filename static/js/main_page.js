const url = new URL(window.location.href);
const telegram_id = atob(url.searchParams.get("student_id"));
console.log(telegram_id);
localStorage.setItem("telegram_id", telegram_id);