# Currency Converter using current stocks  
To use run `pip install currconver`  
Or if your on an Apple Silicon (AArch64) Mac you can install it without python using  
`curl -sSL https://raw.githubusercontent.com/Wdboyes13/currencyconverter/refs/heads/main/cli/install.sh | bash`  
To configure API Key  
at ~/.config/currconver/config.json  
```js  
{  
    "KEY": "Your Open Exchange Rates API Key"  
}  
```  
Key can be gotten at https://openexchangerates.org/signup/free  
For conversion run `python3 -m currconver CONV local_currency destination_currency amount_decimal`