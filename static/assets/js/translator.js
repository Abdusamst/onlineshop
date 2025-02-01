function googleTranslateElementInit() {
    new google.translate.TranslateElement({ pageLanguage: 'ru' }, 'google_translate_element');
}

function changeLanguage(lang) {
    var select = document.querySelector(".goog-te-combo");
    if (select) {
        select.value = lang;
        select.dispatchEvent(new Event("change"));
    }
}
