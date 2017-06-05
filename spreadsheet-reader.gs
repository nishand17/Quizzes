function readFromSheet() {
  var sheet = SpreadsheetApp.openByUrl('https://docs.google.com/spreadsheets/d/12lofWvDfhslU2abn407SwK41feHcZWiAQcRgsKtzHnc/edit#gid=0');
  var setupSheetValues = sheet.getDataRange().getValues();
  var rowNum = sheet.getDataRange().getLastRow()-1;
  var form = FormApp.create(setupSheetValues[rowNum][0]).setTitle(setupSheetValues[rowNum][0]).setIsQuiz(true);
  
  var quizSheet = SpreadsheetApp.openByUrl(setupSheetValues[rowNum][1]);
  var quizSheetValues = quizSheet.getDataRange().getValues();
  
  form.addSectionHeaderItem().setTitle(quizSheetValues[1][1]).setHelpText(quizSheetValues[1][3]); // WELCOME
  
  for(var i = 2; i < quizSheet.getDataRange().getLastRow(); i++) {
    if(quizSheetValues[i][2].trim().toLowerCase() != quizSheetValues[i-1][2].trim().toLowerCase()) { //New Section
      form.addPageBreakItem().setTitle(quizSheetValues[i][2]).setHelpText(quizSheetValues[i][3]);
    }
    
    switch(quizSheetValues[i][0].toString().trim().toLowerCase()) {
      case 'question':
        if(quizSheetValues[i][4].toString().trim().toLowerCase() != 'none') {
          var pathArr = quizSheetValues[i][4].toString().split("/");
          var image = null;
          if(pathArr.length == 1) {
            image = DriveApp.getFilesByName(pathArr[0]).next();
          }
          else {
            var rootFolder = DriveApp.getFoldersByName(pathArr[0]).next();
            
            for(var folderIter = 1; folderIter < pathArr.length-1; folderIter++) {
              rootFolder = rootFolder.getFoldersByName(pathArr[folderIter]).next();
            }
            image = rootFolder.getFilesByName(pathArr[pathArr.length-1]).next();
          }
          form.addImageItem().setImage(image);
          
        }
        break;
    }
  }
  Logger.log(form.getPublishedUrl());
    
}
