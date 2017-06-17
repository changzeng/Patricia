Patricia
====
Hello guys,this is a simple interpreter designed by myself.<br>
This readme file only contains some introductory information about the project.<br>
If you want to know more detail about this project.Please visit my personal home page [http://www.geekliao.cn](http://www.geekliao.cn).<br>
***
This interpreter only contains three parts now.They are Lexer Parser and SemanticAnalyzer.(I'll add the other components in the next few weeks and then I'll update my blog and this readme tutorial).<br>
Acknowledgement
====
The reaseon of why I decided to design an interpreter is I want to know how compiler works.Even though I have studied *<font color="red">The Theory Of Compiler</font>* still I have no idea about what compiler exactly works until I have written my first compiler followed by a blog.<br>
This is the address of that blog *[Let’s Build A Simple Interpreter by Ruslan Spivak](https://ruslanspivak.com/lsbasi-part1/)*.If you have ever read both my blog and this blog you'll know the theory behind these two interpreter is same.But my interpreter is more complex cause I have added more grammer rules.<br>
Besides,I beleve the theory of compiler is related with both NLP and NLU.All of their goals are extract infromation from plain text.To make computer understand our languages.We must convert our language to another format which computer can process.So this can be though as a process to convert a language to another language.That is what compiler indeed do.<br>
Lexer
---
The functionality of Lexer is to convert the source code to seperate tokens one by one.Token is minimum meaningful unit of the source code.<br>
The core function of Lexer is getNextToken().Rather than obtained all tokens instantly our interpreter only take one token at each time.Since obtained all tokens instantly in expensive and unnecessary cause we need allocate a block of memory to store them.If the source code is very very long when only decide to call the lexer the memory was run out no mention to parse the programe.<br>
Paerser
---
The functionality of Parser is using the tokens to build an abstract syntax tree(AST).<br>
The algorithm I used to build this interpreter is recursive descent and is similar to LL(1).Rather than using the first char to determine which direction to descent in LL(1) our algorithm used the current token.<br>
As a result our Parser returned an AST.
SemanticAnalyzer
---
Having built the AST still we wouldn't know wheter our program is make sense.<br>
For example:<br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
*int a  =  "abc";*<br>
This is obviously wrong cause we assign a string to an integer variable.It wouldn't be makeing sense even the lexical analyze of this statement is right.<br>
Having gotten that,you may want to ask why we perform a separate semantic process?Why we don't perfome semantic analyze simultaneously with lexical analyze?<br>
In fact,the above sentence is special case which is too simple to cover all kinds of situation.Consider the following case:<br>
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
*int a = getNext()+a[0];*<br>
In this case we couldn't know wheter the sentence is make sense by considering only this sentence in count cause we need more information.But we don't know where to get the information.So we need a separate process to determine wheter the program is make sense by take the whole program in count.<br>