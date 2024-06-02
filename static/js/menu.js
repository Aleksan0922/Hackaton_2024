var IsOpen = false

function chmod() {

    if (IsOpen) {
        document.getElementById('menu-mobile').style.marginTop = '0px'
        IsOpen = false
    } else {
        document.getElementById('menu-mobile').style.marginTop = 'calc(((44px * 3) + (14px * 2) + 52px) * -1)'
        IsOpen = true
    }
}

chmod()