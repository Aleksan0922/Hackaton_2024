var testmask = new IMask(
    document.getElementById('test-input'),
    {
        mask: Number,
        scale: 5,
        thousandsSeparator: ' ',
        radix: ',',
        mapToRadix: ['.']
    }
)

function input() {
    if (document.querySelector('#test-input').value.includes(',')) {
        document.querySelector('#num-panel-point').style = 'opacity: .5;pointer-events: none;'
    } else {
        document.querySelector('#num-panel-point').style = 'opacity: 1;pointer-events: all;'
    }

    if (document.querySelector('#test-input').value.includes('-')) {
        document.querySelector('#num-panel-minus').style = 'opacity: .5;pointer-events: none;'
    } else {
        document.querySelector('#num-panel-minus').style = 'opacity: 1;pointer-events: all;'
    }

    if (document.querySelector('#test-input').value.length == 0) {
        document.querySelector('#num-panel-erase').style = 'opacity: .5;pointer-events: none;'
    } else {
        document.querySelector('#num-panel-erase').style = 'opacity: 1;pointer-events: all;'
    }
}

function erase() {
    document.querySelector('#test-input').value = ''
    input()
    testmask.updateValue();
    testmask.updateControl();
}

function addE(symv) {
    document.getElementById('test-input').value += symv

    input()

    if (symv != ',') {
        testmask.updateValue();
        testmask.updateControl();
    }
}

input()

document.querySelector('#test-input').addEventListener('input', input)