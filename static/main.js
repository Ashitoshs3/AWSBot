function output(input) {
  let text = input.toLowerCase().replace(/[^\w\s\d]/gi, "");

  text = text
    .replace(/[\W_]/g, " ")
    .replace(/ a /g, " ")
    .replace(/i feel /g, "")
    .replace(/whats/g, "what is")
    .replace(/please /g, "")
    .replace(/ please/g, "")
    .trim();

  // If EC2 or S3 are mentioned, ask the TAPAS model
  if (text.includes("s3") || text.includes("ec2") || text.includes("bucket")) {
    call_to_ai(input, text);
  } else {
    addChat(input, "Sorry! I didn't get you. Please ask about AWS services.");
  }
}

function call_to_ai(input, message) {
  const mainDiv = document.getElementById("message-section");
  let userDiv = document.createElement("div");
  userDiv.id = "popup";
  userDiv.classList.add("message");
  userDiv.innerHTML = `<span id="user-response">Generating...</span>`;
  mainDiv.appendChild(userDiv);

  var scroll = document.getElementById("message-section");
  scroll.scrollTop = scroll.scrollHeight;

  // Send query to the backend
  $.ajax({
    url: '/chat/ask',
    type: 'POST',
    contentType: 'application/json',
    data: JSON.stringify({ 'chat_box_input': message }),
    success: function (response) {
      userDiv.remove();
      generated_output = response.answer;
      if (response.answer == "") {
        generated_output = "Unfortunately, I don't have access to that information at the moment. Is there anything else I can help you with?";
      }
      addChat(input, generated_output);
    },
    error: function (error) {
      console.log(error);
      userDiv.remove();
      addChat(input, "Error: My brain is not working properly. Restart me.");
    }
  });
}
