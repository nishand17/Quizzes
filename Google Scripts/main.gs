function readFromSheet(quizNum) { // 1-numQuizzes
  var sheet = SpreadsheetApp.openByUrl(getUrl());
  var setupSheetValues = sheet.getDataRange().getValues();
  var rowNum = parseInt(quizNum);  
  Logger.log(setupSheetValues[rowNum][4].substring(0,5));
  if(setupSheetValues[rowNum][4].substring(0,5) == 'https') {
    Logger.log("Existing sheet");
    var existingArr = [];
    existingArr.push(setupSheetValues[rowNum][4].toString());
    existingArr.push(setupSheetValues[rowNum][5].toString());
    return existingArr;
  }
  Logger.log("Original sheet");
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
            mcItem.setChoices(choiceArr);
            
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
                else listChoiceArr.push(listItem.createChoice(listChoice, false));
                }
            }
            listItem.setChoices(listChoiceArr);
            
            break;
          
          case 'text':
            var textItem = form.addParagraphTextItem().setTitle(quizSheetValues[i][1]).setHelpText(quizSheetValues[i][3]).setPoints(1).setRequired(true);            
            textItem.setGeneralFeedback(generalFeedback);
            break;
          case 'checkbox':
            var checkItem = form.addCheckboxItem().setTitle(quizSheetValues[i][1]).setHelpText(quizSheetValues[i][3]).setPoints(1).setRequired(true);
            var checkChoiceArr = [];
            var checkAnswers = quizSheetValues[i][6].toString().trim().split(",");
            Logger.log(questionArr);
            for(var checkIter = 1; checkIter < questionArr.length; checkIter++) {
              var checkChoice = questionArr[checkIter].toString().trim();
              if(checkAnswers.indexOf(checkChoice) != -1) checkChoiceArr.push(checkItem.createChoice(checkChoice, true));
              else checkChoiceArr.push(checkItem.createChoice(checkChoice, false));
            }
            checkItem.setChoices(checkChoiceArr);
            
            break;
          default: break; 
            
        }
        break;
        
      default:
        break;
    }
  }
  var arr = [];
  var publishCell = sheet.getRange("E"+((rowNum+1).toString())).setValue(form.getPublishedUrl());
  var editCell = sheet.getRange("F"+((rowNum+1).toString())).setValue(form.getEditUrl());
  Logger.log(form.getEditUrl());
  Logger.log(form.getPublishedUrl())
  arr.push(form.getPublishedUrl());
  arr.push(form.getEditUrl());
  return arr;    
}

function getSendInfo(quizNum) {
  // NEED FormLink, RespondentsData - using the good old major sheet
  var sheet = SpreadsheetApp.openByUrl(getUrl());
  var sheetValues = sheet.getDataRange().getValues();
  var rowNum = quizNum;
  var dict = {};
  dict['formUrl'] = sheetValues[rowNum][4].toString();
  var recipientsSheetValues = SpreadsheetApp.openByUrl(sheetValues[rowNum][2].toString()).getDataRange().getDisplayValues();
  dict['respondents'] = recipientsSheetValues;
  dict['description'] = sheetValues[rowNum][6].toString();
  dict['title'] = sheetValues[rowNum][0].toString();
  return dict;
}

function getSendList() {
  var sheet = SpreadsheetApp.openByUrl(getUrl());
  var sheetValues = sheet.getDataRange().getValues();
  var arr = [];
  for(var i = 1; i < sheetValues.length; i++) {
    if(sheetValues[i][0] != "" && sheetValues[i][4] != "" && sheetValues[i][6] != "" && sheetValues[i][2] != "") arr.push(sheetValues[i][0].toString());  
  }
  Logger.log(arr);
  return arr;
}

function getCreateList() {
  var sheet = SpreadsheetApp.openByUrl(getUrl());
  var sheetValues = sheet.getDataRange().getValues();
  var arr = [];
  for(var i = 1; i < sheetValues.length; i++) {
    if(sheetValues[i][0] != "" && sheetValues[i][1] != "") arr.push(sheetValues[i][0].toString());  
  }
  Logger.log(arr)
  return arr;
}

function getGradeList() {
  var sheetValues = SpreadsheetApp.openByUrl(getUrl()).getDataRange().getDisplayValues();
  var arr = [];
  for(var i = 1; i < sheetValues.length; i++) {
    if(sheetValues[i][0] != "" && sheetValues[i][1] != "" && sheetValues[i][3] != "") arr.push(sheetValues[i][0].toString());
  }
  Logger.log(arr);
  return arr;
}

function getResponsesData(quizNum) {
  var sheet = SpreadsheetApp.openByUrl(getUrl());
  var sheetValues = sheet.getDataRange().getDisplayValues();
  var responseData = SpreadsheetApp.openByUrl(sheetValues[quizNum][3].toString()).getDataRange().getDisplayValues();
  Logger.log(responseData);
  return responseData;
}

function getTemplateData(quizNum) {
  var sheet = SpreadsheetApp.openByUrl(getUrl());
  var sheetValues = sheet.getDataRange().getDisplayValues();
  var templateData = SpreadsheetApp.openByUrl(sheetValues[quizNum][1].toString()).getDataRange().getDisplayValues();
  Logger.log(templateData);
  return templateData;
}
function testQuizSheet() {
  readFromSheet(1);
}

function getUrl() {
  return 'https://docs.google.com/spreadsheets/d/12lofWvDfhslU2abn407SwK41feHcZWiAQcRgsKtzHnc/edit#gid=0';
}