document.addEventListener('DOMContentLoaded', function() {

    // Settle the display of forms 
    document.querySelector('#record_form').style.display = 'none';
    document.querySelector('#planned_form').style.display = 'none';
    document.querySelector('#recurrence').disabled = false;
    
    const new_record_button = document.querySelector('#new_record_button');
    const new_planned_button = document.querySelector('#new_planned_button');
    const one_time_payment_button = document.querySelector('#success-outlined-frequency');
    const recurring_payment_button = document.querySelector('#danger-outlined-frequency');

    new_record_button.addEventListener('click', () => show_record_form());
    new_planned_button.addEventListener('click', () => show_planned_form());
    one_time_payment_button.addEventListener('click', () => disable_recurrence());
    recurring_payment_button.addEventListener('click', () => enable_recurrence());

    // Settle the minimum date for the date input
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    document.querySelector('#date').min = tomorrow.toISOString().split("T")[0];
});

function show_record_form() {
    document.querySelector('#record_form').style.display = 'block';
    document.querySelector('#new_record_button').style.display = 'none';
};

function show_planned_form() {
    document.querySelector('#planned_form').style.display = 'block';
    document.querySelector('#new_planned_button').style.display = 'none';
}

function disable_recurrence() {
    document.querySelector('#recurrence').disabled = true;
}

function enable_recurrence() {
    document.querySelector('#recurrence').disabled = false;
}

