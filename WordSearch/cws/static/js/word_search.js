// Javascript file for Find Your Words
// Version 2.0

function swapFont(e) {
    e.preventDefault();
    var currentFont = document.getElementById('font_style');
    var contentBlock = document.getElementById('content_block');
    // console.log('JS script found and swapFont clicked');
    if (currentFont.innerText === 'Sans Serif') {
        console.log('Sans found in text');
        contentBlock.classList.remove('font_sans_serif');
        contentBlock.classList.add('font_serif');
        currentFont.innerText = 'Serif';
    } else {
        console.log(`Sans not found, only ${currentFont.innerText}`);
        contentBlock.classList.remove('font_serif');
        contentBlock.classList.add('font_sans_serif');
        currentFont.innerText = 'Sans Serif';
    }
}

function callPrintView() {
    var currentFont = document.getElementById('font_style');
    if (currentFont.innerText === 'Sans Serif') {
        fontStyle = 'sans_serif';
    } else {
        fontStyle = 'serif';
    }
    window.location.href = `print_view?font_style=${fontStyle}`;
}
