window.addEventListener('load', function() {
    (function ($) {
        if(location.href.indexOf("add")>-1)
            $("#jazzy-tabs .nav-item").last().remove();
        else{
            $("#current-status-tab .card-body").hide();
            var new_html = `
                <script>
                    function summaryButtonclick(){
                        let button = $("#summaryButton");
                        button.text("Loading...");
                        button.prop("disabled", true);

                        // Simulate API call (replace with actual fetch request)
                        setTimeout(() => {
                            let response = 'This is the current summary.';
                            
                            let summaryDiv = document.getElementById("summaryContainer");
                            summaryDiv.innerHTML = response;
                            button.remove();
                        }, 2000); // Simulated delay
                    };
                </script>
                <style>
                    #summaryButton {
                        width: fit-content;
                        margin: 0 auto 20px auto;
                        box-shadow:inset 0px -3px 7px 0px #007bff;
                        background:linear-gradient(to bottom, #2dabf9 5%, #0688fa 100%);
                        background-color:#2dabf9;
                        border-radius:3px;
                        border:1px solid #0b0e07;
                        display:inline-block;
                        cursor:pointer;
                        color:#ffffff;
                        font-family:Arial;
                        font-size:15px;
                        padding:9px 23px;
                        text-decoration:none;
                        text-shadow:0px 1px 0px #263666;
                    }
                    #summaryButton:hover {
                        background:linear-gradient(to bottom, #0688fa 5%, #2dabf9 100%);
                        background-color:#0688fa;
                    }
                    #summaryButton:active {
                        position:relative;
                        top:1px;
                    }
                </style>
                <button id="summaryButton" type="button" onclick="summaryButtonclick();">Request Current Summary</button>
                <div id="summaryContainer"></div>
            `;
            $("#current-status-tab .card").append(new_html);
        }
        setTimeout(function() {
            $("br").nextAll().hide();
            $(".datetime br").hide();
            $(".datetime").contents().filter(function() {
                return this.nodeType === 3;  // Node type 3 is for text nodes
            }).each(function() {
                if($(this).text().indexOf("Time")>-1) $(this).remove();  // Remove text nodes
            });
            $("#id_next_appointment_0").on("input", function() {
                // Check if the value of id_next_appointment_0 is blank
                if ($(this).val().trim() === "") {
                    // If it's blank, set the value of id_next_appointment_1 to blank
                    $("#id_next_appointment_1").val("");
                } else {
                    // Otherwise, set id_next_appointment_1 to 11:11:11
                    $("#id_next_appointment_1").val("11:11:11");
                }
            });
            setInterval(function(){
                if ($("#id_next_appointment_0").val().trim() === "") {
                    // If it's blank, set the value of id_next_appointment_1 to blank
                    $("#id_next_appointment_1").val("");
                } else {
                    // Otherwise, set id_next_appointment_1 to 11:11:11
                    $("#id_next_appointment_1").val("11:11:11");
                }
            },300);
        }, 500);
    })(django.jQuery);
});