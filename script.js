$(document).ready(function(){ 
    // when document is first loaded, selection is set to "No". hide custom tip bar and show next page button without text box. 
    $('#div1').show();
    $('#custom_tip').hide();
    $('#slider_value').text('0')
    $('#dollar_amt').html('0.00');

    
    // when selection is changed to "Yes". Display text box
    $( "#purpose" ).change(function() {
        var selection = $(this).val();
        if (selection == 'yes')
        { 
            $('#div2').show();
            $('#div1').hide();
        }
    });

    // when selection is changed back to "No". Hide text box
    $( "#purpose" ).change(function() {
        var selection = $(this).val();
        if (selection == 'no')
        {
            $('#div2').hide();
            $('#div1').show();
        }
    });

    // when custom tip check box is checked show the range dial
    $( "#customtip" ).change(function() {
        $('#custom_tip').toggle();
    });

    // dynamically display the percent number as bar moves
    $( "#slider" ).change(function() {
        $('#slider_value').html( $(this).val() );
        // converting jinja variable to javascript type
        var sub = {{ subtotal|tojson|safe }};
        // math calculation 
        tipdollar = ($(this).val() / 100) * sub;
        tipdollar = tipdollar.toFixed(2);
        $('#dollar_amt').html( tipdollar );
    });

});
