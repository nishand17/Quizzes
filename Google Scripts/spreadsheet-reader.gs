function readFromSheet() {
  var sheet = SpreadsheetApp.openByUrl('https://docs.google.com/spreadsheets/d/12lofWvDfhslU2abn407SwK41feHcZWiAQcRgsKtzHnc/edit#gid=0');
  var setupSheetValues = sheet.getDataRange().getValues();
  var rowNum = sheet.getDataRange().getLastRow()-1;
  var form = FormApp.create(setupSheetValues[rowNum][0]).setTitle(setupSheetValues[rowNum][0]).setIsQuiz(true);
  var questionNum = 1;
  var quizSheet = SpreadsheetApp.openByUrl(setupSheetValues[rowNum][1]);
  var quizSheetValues = quizSheet.getDataRange().getValues();
  
  var correctFeedback = FormApp.createFeedback().setText("Good Job! You were correct!").build();
  var generalFeedback = FormApp.createFeedback().setText("Your graded response will be sent via email soon").build();
  
  form.addSectionHeaderItem().setTitle(quizSheetValues[1][1]).setHelpText(quizSheetValues[1][3]); // WELCOME
  
  for(var i = 2; i < quizSheet.getDataRange().getLastRow(); i++) {
    if(quizSheetValues[i][2].trim().toLowerCase() != quizSheetValues[i-1][2].trim().toLowerCase()) { //New Section
      form.addPageBreakItem().setTitle(quizSheetValues[i][2]).setHelpText(quizSheetValues[i][3]);
    }
    
    switch(quizSheetValues[i][0].toString().trim().toLowerCase()) {
      case 'question':
        form.addSectionHeaderItem().setTitle("Question " + questionNum++);
        if(quizSheetValues[i][4].toString().trim().toLowerCase() != 'none') {
          var paths = quizSheetValues[i][4].toString().split(",");
          for(var imgIter = 0; imgIter < paths.length; imgIter++) {
            var pathArr = paths[imgIter].split("/");
            var image = null;
            if(pathArr.length == 1) {
              image = DriveApp.getFilesByName(pathArr[0]).next();
            }
            else {
              var rootFolder = DriveApp.getFoldersByName(pathArr[0].trim()).next();
              
              for(var folderIter = 1; folderIter < pathArr.length-1; folderIter++) {
                rootFolder = rootFolder.getFoldersByName(pathArr[folderIter]).next();
              }
              image = rootFolder.getFilesByName(pathArr[pathArr.length-1]).next();
            }
            var title = pathArr[pathArr.length-1];
            form.addImageItem().setImage(image).setTitle(title.substring(0,title.length-4));
          }
        }
        var questionArr = quizSheetValues[i][5].toString().split(",");
        switch(questionArr[0].trim().toLowerCase()) {
          case 'multiplechoice':
            var mcItem = form.addMultipleChoiceItem().setTitle(quizSheetValues[i][1]).setHelpText(quizSheetValues[i][3]).setPoints(1).setRequired(true);
            var choiceArr = [];
            var answer = quizSheetValues[i][6].toString().trim();
            for(var choiceIter = 1; choiceIter < questionArr.length; choiceIter++) {
              var choice = questionArr[choiceIter].trim();              
              if(choice == answer) choiceArr.push(mcItem.createChoice(choice, true));
              else choiceArr.push(mcItem.createChoice(choice, false));
            }
            mcItem.setChoices(choiceArr).setFeedbackForCorrect(correctFeedback);
            var incorrectFeedbackMC = FormApp.createFeedback().setText("Sorry, the correct answer was " + answer).build();
            mcItem.setFeedbackForIncorrect(incorrectFeedbackMC);
            
            break;
          case 'dropdown':
            var listItem = form.addListItem().setTitle(quizSheetValues[i][1]).setHelpText(quizSheetValues[i][3]).setPoints(1).setRequired(true);
            var listChoiceArr = [];
            var listAnswer = quizSheetValues[i][6].toString().trim();
            for(var listIter = 1; listIter < questionArr.length; listIter++) {
              var listChoice = questionArr[listIter];
              
              if((listChoice.length > 5) && (listChoice.substring(0, 5) == "range")) { //range(0,100)
                var ranges = listChoice.substring(6,listChoice.length-1).split(">");
                var start = parseInt(ranges[0].trim());
                var end = parseInt(ranges[1].trim());        
                listAnswer = parseInt(listAnswer);
                for(var rangeIter = start; rangeIter <= end; rangeIter++) {
                 
                  if(rangeIter == listAnswer) listChoiceArr.push(listItem.createChoice(rangeIter.toString(), true));
                  else listChoiceArr.push(listItem.createChoice(rangeIter.toString(), false));
                }                                                                      
              }
              else {
                if(listChoice.toString() == listAnswer.toString()) listChoiceArr.push(listItem.createChoice(listChoice, true));
                else listChoiceArr.push(listItem.createChoice(listChoice, false))
                }
            }
            listItem.setChoices(listChoiceArr).setFeedbackForCorrect(correctFeedback);
            var incorrectFeedbackDD = FormApp.createFeedback().setText("Sorry, the correct answer was " + listAnswer).build();
            listItem.setFeedbackForIncorrect(incorrectFeedbackDD);
            break;
          case 'text':
            var textItem = form.addParagraphTextItem().setTitle(quizSheetValues[i][1]).setHelpText(quizSheetValues[i][3]).setPoints(1).setRequired(true);            
            textItem.setGeneralFeedback(generalFeedback);
          case 'checkbox':
            var checkItem = form.addCheckboxItem().setTitle(quizSheetValues[i][1]).setHelpText(quizSheetValues[i][3]).setPoints(1).setRequired(true);
            var checkChoiceArr = [];
            var checkAnswers = quizSheetValues[i][6].toString().trim().split(",");
            for(var checkIter = 1; checkIter < questionArr.length; checkIter++) {
              if(checkAnswers.indexOf(questionArr[checkIter].trim()) != -1) checkChoiceArr.push(checkItem.createChoice(questionArr[choiceIter], true));
              else checkChoiceArr.push(checkItem.createChoice(questionArr[choiceIter], false));
            }
            checkItem.setChoices(checkChoiceArr);
            checkItem.setFeedbackForCorrect(correctFeedback);
            var incorrectFeedbackCB = FormApp.createFeedback().setText("Sorry, the correct answers were " + checkAnswers.toString());
            
          default: break; 
            
        }
        break;
        
      default:
        break;
    }
  }
  Logger.log(form.getPublishedUrl());
  Logger.log(form.getEditUrl());
    
}
