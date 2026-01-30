// Javascript file for Find Your Words
// Version 2.0

function swapFont(e) {
    e.preventDefault();
    var currentFont = document.getElementById('font_selector');
    var contentBlock = document.getElementById('content_block');
    var hiddenFontStyle = document.getElementById('font_style');
    var getFontStyle = document.getElementById('change_link');
    // console.log('JS script found and swapFont clicked');
    if (currentFont.innerText === 'Sans Serif') {
        console.log('Sans found in text');
        contentBlock.classList.remove('font_sans_serif');
        contentBlock.classList.add('font_serif');
        currentFont.innerText = 'Serif';
        if (hiddenFontStyle) {
            hiddenFontStyle.value = "serif";
        }
        if (getFontStyle) {
            var fontUrl = getFontStyle.getAttribute('href');
            newFontUrl = fontUrl.replace("=sans_serif", "=serif");
            getFontStyle.setAttribute('href', newFontUrl);
        }
    } else {
        console.log(`Sans not found, only ${currentFont.innerText}`);
        contentBlock.classList.remove('font_serif');
        contentBlock.classList.add('font_sans_serif');
        currentFont.innerText = 'Sans Serif';
        if (hiddenFontStyle) {
            hiddenFontStyle.value = "sans_serif";
        }
        if (getFontStyle) {
            var fontUrl = getFontStyle.getAttribute('href');
            newFontUrl = fontUrl.replace("=serif", "=sans_serif");
            getFontStyle.setAttribute('href', newFontUrl);
        }
    }
}

function callPrintView() {
    var currentFont = document.getElementById('font_selector');
    if (currentFont.innerText === 'Sans Serif') {
        fontStyle = 'sans_serif';
    } else {
        fontStyle = 'serif';
    }
    window.open(`print_view?font_style=${fontStyle}`, "_blank");
}

window.onload = function() {
    var wordForm = document.getElementById('id_words');
    var wordCollectionForm = document.getElementById('id_word_collection');

    if (wordForm && wordCollectionForm) {
        wordForm.addEventListener('keyup', function() {
            var wordFormUpper = wordForm.value.toUpperCase();
            wordForm.value = wordFormUpper;
        })
        wordCollectionForm.addEventListener('keyup', function () {
            var wordCollectionFormUpper = wordCollectionForm.value.toUpperCase();
            wordCollectionForm.value = wordCollectionFormUpper;
        })
    }
}
