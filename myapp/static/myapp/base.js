$(document).ready(function() {
    var currentQuestionIndex = 0;
    var totalQuestions = parseInt($('#progress').attr('value'));
    var answers = {};
    var answer_list = [];
    
    $('.question').hide();
    $('#question-0').show();
    
    $('.answer-btn').click(function() {
        var currentQuestion = $('#question-' + currentQuestionIndex);
        var nextQuestionIndex = currentQuestionIndex + 1;
        var nextQuestion = $('#question-' + nextQuestionIndex);

        var id = $(this).attr('id');
        var currentAnswer = $("#" + id).attr("value");

        // Hide the current question and show the next one
        currentQuestion.hide();
        nextQuestion.show();
        
        // Update the progress bar or display a message if it's the last question
        if (nextQuestionIndex === totalQuestions) {
            answers["answers"] = answer_list;
            $('#progress').text('Completed! We have received your answers.');
            $('#next-btn').hide();
            $.ajax({
                url: 'screener-endpoint',
                type: 'POST',
                data: JSON.stringify(answers),
                contentType: 'application/json',
                success: function(response) {
                  console.log('Answers submitted successfully');
                  console.log(answers);
                },
                error: function(error) {
                  console.error('Error submitting answers:', error);
                }
              });
        } else {
            $('#progress').text((nextQuestionIndex + 1) + ' / ' + totalQuestions);
        }

        var question_id = currentQuestion.attr("value");
        var answer_id = parseInt(currentAnswer);
        answer_list.push({"value": answer_id, "question_id": question_id})

        currentQuestionIndex = nextQuestionIndex;
    });
});