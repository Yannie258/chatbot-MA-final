/**
 * @param {number} x
 * @return {boolean}
 */
var isPalindrome = function(x) {
    let s = x.toString();
    //console.log(s.length /2);
    let pivot = Math.floor(s.length / 2);
    console.log(pivot);
    if(s.length < 2) return true;
    if(s.length < 3 && s[0] === s[1]) return true;
    if(s.length >3){
        for(let i = 0; i < pivot; i++) {
        console.log('test', s[i]);
        for(let j = s.length-1 ; j > pivot; j--){
            console.log('test2', s[j]);
            if(s[i] === s[j]) return true;
            else return false;

        }
            return;
        
        }  
    }
    
};
isPalindrome(121);