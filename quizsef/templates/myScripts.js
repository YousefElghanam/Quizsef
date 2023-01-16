
                const myText{{row+1}} = document.getElementById("question{{row+1}}");
                myText{{row+1}}.style.cssText = `height: ${myText{{row+1}}.scrollHeight}px; overflow-y: hidden`;

                myText{{row+1}}.addEventListener("input", function(){
                    this.style.height = "auto";
                    this.style.height = `${this.scrollHeight}px`;
                });
                
                const myText{{row+1}}1 = document.getElementById("answer{{row+1}}-1");
                myText{{row+1}}1.style.cssText = `height: ${myText{{row+1}}1.scrollHeight}px; overflow-y: hidden`;

                myText{{row+1}}1.addEventListener("input", function(){
                    this.style.height = "auto";
                    this.style.height = `${this.scrollHeight}px`;
                });
                const myText{{row+1}}2 = document.getElementById("answer{{row+1}}-2");
                myText{{row+1}}2.style.cssText = `height: ${myText{{row+1}}2.scrollHeight}px; overflow-y: hidden`;

                myText{{row+1}}2.addEventListener("input", function(){
                    this.style.height = "auto";
                    this.style.height = `${this.scrollHeight}px`;
                });
                const myText{{row+1}}3 = document.getElementById("answer{{row+1}}-3");
                myText{{row+1}}3.style.cssText = `height: ${myText{{row+1}}3.scrollHeight}px; overflow-y: hidden`;

                myText{{row+1}}3.addEventListener("input", function(){
                    this.style.height = "auto";
                    this.style.height = `${this.scrollHeight}px`;
                });
                const myText{{row+1}}4 = document.getElementById("answer{{row+1}}-4");
                myText{{row+1}}4.style.cssText = `height: ${myText{{row+1}}4.scrollHeight}px; overflow-y: hidden`;

                myText{{row+1}}4.addEventListener("input", function(){
                    this.style.height = "auto";
                    this.style.height = `${this.scrollHeight}px`;
                });
                const rightAnswer = document.getElementById("rightanswer");
                rightAnswer.style.cssText = `height: ${rightAnswer.scrollHeight}px; overflow-y: hidden`;

                rightAnswer.addEventListener("input", function(){
                    this.style.height = "auto";
                    this.style.height = `${this.scrollHeight}px`;
                });

            