const { createApp } = Vue
createApp({
    data() {
        return {
            nums: [1,2,3,4,5,6,7,8,9],
            x2: []
        }
    },
    methods: {
        //[{“genre”: genre name, “shown”: true},...]
        async keyPressRouter(event) {
            switch (event.which) {
                case 13:
                    this.Print();
                    break;
                case 49:
                    $('.Selected').text('1');
                    $('.Selected').removeClass('Selected');
                    break;
                case 50:
                    $('.Selected').text('2');
                    $('.Selected').removeClass('Selected');
                    break;
                case 51:
                    $('.Selected').text('3');
                    $('.Selected').removeClass('Selected');
                    break;
                case 52:
                    $('.Selected').text('4');
                    $('.Selected').removeClass('Selected');
                    break;
                case 53:
                    $('.Selected').text('5');
                    $('.Selected').removeClass('Selected');
                    break;
                case 54:
                    $('.Selected').text('6');
                    $('.Selected').removeClass('Selected');
                    break;
                case 55:
                    $('.Selected').text('7');
                    $('.Selected').removeClass('Selected');
                    break;
                case 56:
                    $('.Selected').text('8');
                    $('.Selected').removeClass('Selected');
                    break;
                case 57:
                    $('.Selected').text('9');
                    $('.Selected').removeClass('Selected');
                    break;
                case 70:
                    this.adjust();
                    break;
            }
        },
        Selected(elem){
            $('.Selected').removeClass('Selected');
            elem.target.classList.add('Selected');
            
        },
        Updated(elem){
            $('.Selected').text(elem.target.innerHTML);
            $('.Selected').removeClass('Selected');
        },
        Erased(elem){
            $('.Selected').text('');
            $('.Selected').removeClass('Selected');
        },
        async Print(){
            c = 0;
            var x2 = [];
            while(x2.length < 81){
                for(var k = 0; k < 3; k++){
                    for(var j = 0; j < 3; j++){
                    x2.push(c);
                    c++;
                    x2.push(c);
                    c++;
                    x2.push(c);
                    c += 7;
                    }
                    c -= 24;
                }
                c+= 18;
            }
            this.x2 = x2;
            x = ['0','1','2','3','4','5','6','7','8','9'];
            y = '';
            z = [$('.grid-item')];
            // console.log(z[0].text());
            // z[0][0].getInnerHTML();
            for(var i = 0; i < x2.length; i++){
                if(z[0][x2[i]].getInnerHTML() in x){
                    y += z[0][x2[i]].getInnerHTML();
                } 
                else{
                    y += '0';
                }
            }
            console.log(y);
            await $.ajax({
                url: "/test",
                type:"POST",
                contentType:"application/json",
                data: JSON.stringify(y)
            }).then((res)=>{ lol = res['answer'] });
            this.adjust(lol);
        },
        async adjust(ans){
            c = 0;
            z = [$('.grid-item')];
            for(var i = 0; i < this.x2.length; i++){
                z[0][this.x2[i]].innerHTML = ans[i]; 
            }
            console.log("DONE");
        }
    },
    mounted(){
        $(window).keydown(this.keyPressRouter);
    }
}).mount('#app')
//document.getElementById('app').__vue_app__._instance.data
//document.getElementById('app').__vue_app__._instance.data.data_arr = ans;


// Active tabs, Active Dropdown selection, Active filter selection
