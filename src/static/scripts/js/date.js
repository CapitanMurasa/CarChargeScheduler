const dateBookPickerId = document.getElementById("dateBookPicker");
const dateDuePickerId = document.getElementById("dateDuePicker");

function ReturnTodayDate(){
    const localDate = new Date();
    localDate.setMinutes(localDate.getMinutes() - localDate.getTimezoneOffset());
    return localDate.toISOString().slice(0, 16);
}
dateBookPickerId.value = ReturnTodayDate();
dateDuePickerId.value = ReturnTodayDate();
dateBookPickerId.min = ReturnTodayDate();
dateDuePickerId.min = ReturnTodayDate();