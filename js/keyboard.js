var MaskNum = new IMask(
    document.getElementById('test-input'),
    {
      mask: Number,
      thousandsSeparator: ' '
    }
)

function addE(symv) {
    document.getElementById('test-input').value += symv;
    MaskNum.updateValue();
    MaskNum.updateControl();
}