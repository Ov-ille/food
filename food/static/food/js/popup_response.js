const responseData = JSON.parse(document.getElementById('popup_response_data').dataset.popupResponse);
opener.getDataFromPopup(window, responseData.add_change, responseData.id, responseData.text)
