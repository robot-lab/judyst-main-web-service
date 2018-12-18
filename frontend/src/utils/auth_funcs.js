

function CheckRegModel(model) {
    return model.password != '' &&
           model.email.indexOf('@') > -1 &&     
           model.firstName != '' &&     
           model.LastName != '';      
    
}


function isUserExistError(err){
    return err.code == 400 && err.message == 'user already exist'; 
}

export default {
    CheckRegModel,
    isUserExistError
}



