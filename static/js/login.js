function dologin()
{
    var publickeye = document.getElementById("pubkeye").value();
    var publickeyn = document.getElementById("pubkeyn").value();
    var login_form = document.getElementById("login_form");
    pube = (publickeye.substring(2));
    pubn = (publickeyn.slice(2,-1));
    setMaxDigits(130);
    var password = document.getElementById("password").value();
    var key = new RSAKeyPair(pube,"",pubn);
    var en_password = encryptedString(key,password);
    document.getElementById("password").value = en_password;
    login_form.submit();
}