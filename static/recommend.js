$(document).ready(function () {
        $('#search-box').on('input', function () {
            var query = $(this).val();

            $.ajax({
                url: '/autosuggest',
                type: 'POST',
                data: {query: query},
                success: function (response) {
                    var suggestions = response.split(',');

                    var suggestionsHtml = suggestions.map(function (suggestion) {
                        return '<div class="suggestion" onclick="selectSuggestion(\'' + suggestion.trim() + '\')">' + suggestion.trim() + '</div>';
                    }).join('');

                    $('#suggestions-container').html(suggestionsHtml);

                    // Show/hide the suggestions container based on whether there are suggestions
                    if (suggestions.length > 0) {
                        $('#suggestions-container').addClass('active');
                    } else {
                        $('#suggestions-container').removeClass('active');
                    }
                },
                error: function (xhr, status, error) {
                    console.error('Error:', error);
                }
            });
        });
    });

    // Function to handle suggestion selection
    function selectSuggestion(selectedSuggestion) {
        $('#search-box').val(selectedSuggestion);
        $('#suggestions-container').removeClass('active'); // Hide suggestions container after selection
    }