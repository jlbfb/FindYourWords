// Javascript file for Find Your Words
// Version 2.0

function swapFont(e) {
    e.preventDefault();
    var currentFont = document.getElementById('font_selector');
    var contentBlock = document.getElementById('content_block');
    var hiddenFontStyle = document.getElementById('font_style');
    var getFontStyle = document.getElementById('change_link');
    if (currentFont.innerText === 'Sans Serif') {
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
    var listPosition = document.getElementById('list_position').value;
    if (currentFont.innerText === 'Sans Serif') {
        fontStyle = 'sans_serif';
    } else {
        fontStyle = 'serif';
    }
    window.open(`print_view?font_style=${fontStyle}&list_position=${listPosition}`, "_blank");
}

function boardPosition(newPosition) {
    var listPosition = document.getElementById('list_position');
    listPosition.value = newPosition;
    gameContainerTB = document.getElementById('game_container_tb');
    gameContainerLR = document.getElementById('game_container_lr');
    if (newPosition.includes('left') || newPosition.includes('right')) {
        if (newPosition == 'left') {
            gameContainerLR.classList.remove('flex-row-reverse');
        } else if (newPosition == 'right') {
            gameContainerLR.classList.add('flex-row-reverse');
        }
        gameContainerTB.classList.remove('d-flex', 'flex-column-reverse');
        gameContainerTB.classList.add('d-none');
        gameContainerLR.classList.remove('d-none');
    } else if (newPosition.includes('top') || newPosition.includes('bottom')) {
        if (newPosition == 'top') {
            gameContainerTB.classList.remove('d-flex', 'flex-column-reverse');
        } else if (newPosition == 'bottom') {
            gameContainerTB.classList.add('d-flex', 'flex-column-reverse');
        }
        gameContainerLR.classList.add('d-none');
        gameContainerTB.classList.remove('d-none');
    }
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
