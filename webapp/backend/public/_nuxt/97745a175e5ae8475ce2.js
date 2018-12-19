(window.webpackJsonp=window.webpackJsonp||[]).push([[2],{169:function(e,i,a){var t=a(182);"string"==typeof t&&(t=[[e.i,t,""]]),t.locals&&(e.exports=t.locals);(0,a(43).default)("d4be674c",t,!0,{})},181:function(e,i,a){"use strict";var t=a(169);a.n(t).a},182:function(e,i,a){(e.exports=a(42)(!1)).push([e.i,"h4{margin-top:3px}",""])},183:function(e,i,a){"use strict";a.r(i);a(41);var t=a(6),r=a.n(t),n=(a(64),{data:function(){return{showSimilarities:!1,chart:[],locked:!1,ranking:2,similarity:[5,50],similarityOptions:{min:0,max:100,tooltip:"hover",formatter:"{value}%"},ngramMatches:[1e3,9e3],ngramMatchesOptions:{min:0,max:1e4,tooltip:"hover"},chartSize:100,chartSizeOptions:{min:10,max:200,tooltip:"hover"}}},created:function(){this.updateTable()},methods:{alert:function(){window.alert("lol")},log:function(e){console.log(e)},formatDecimal:function(e){return(e/1).toFixed(2).replace(",",".")},updateTable:function(){var e=r()(regeneratorRuntime.mark(function e(){var i;return regeneratorRuntime.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:return this.locked=!0,e.next=3,this.$axios.$get("/ws/search",{params:{rankingType:this.ranking,similarityMin:this.similarity[0],similarityMax:this.similarity[1],ngramsMin:this.ngramMatches[0],ngramsMax:this.ngramMatches[1],size:this.chartSize}});case 3:i=e.sent,this.chart=i,this.locked=!1;case 6:case"end":return e.stop()}},e,this)}));return function(){return e.apply(this,arguments)}}()}}),s=(a(181),a(21)),l=Object(s.a)(n,function(){var e=this,i=e.$createElement,a=e._self._c||i;return a("div",{staticClass:"container"},[a("div",{staticClass:"row"},[a("div",{staticClass:"col-sm-3"},[a("h4",[e._v("Chart size")]),e._v(" "),a("vue-slider",e._b({ref:"slider",attrs:{disabled:e.locked},on:{"drag-end":e.updateTable},model:{value:e.chartSize,callback:function(i){e.chartSize=i},expression:"chartSize"}},"vue-slider",e.chartSizeOptions,!1)),e._v(" "),a("h4",[e._v("Similarity range")]),e._v(" "),a("vue-slider",e._b({ref:"slider",attrs:{disabled:e.locked},on:{"drag-end":e.updateTable},model:{value:e.similarity,callback:function(i){e.similarity=i},expression:"similarity"}},"vue-slider",e.similarityOptions,!1)),e._v(" "),a("label",[a("input",{directives:[{name:"model",rawName:"v-model",value:e.showSimilarities,expression:"showSimilarities"}],attrs:{type:"checkbox"},domProps:{checked:Array.isArray(e.showSimilarities)?e._i(e.showSimilarities,null)>-1:e.showSimilarities},on:{change:function(i){var a=e.showSimilarities,t=i.target,r=!!t.checked;if(Array.isArray(a)){var n=e._i(a,null);t.checked?n<0&&(e.showSimilarities=a.concat([null])):n>-1&&(e.showSimilarities=a.slice(0,n).concat(a.slice(n+1)))}else e.showSimilarities=r}}}),e._v(" Show most similar song\n      ")]),e._v(" "),a("h4",[e._v("N-gram matches")]),e._v(" "),a("vue-slider",e._b({ref:"slider",attrs:{disabled:e.locked},on:{"drag-end":e.updateTable},model:{value:e.ngramMatches,callback:function(i){e.ngramMatches=i},expression:"ngramMatches"}},"vue-slider",e.ngramMatchesOptions,!1)),e._v(" "),a("h4",[e._v("Ranking")]),e._v(" "),a("ul",{staticClass:"list-unstyled"},[a("li",[a("label",[a("input",{directives:[{name:"model",rawName:"v-model",value:e.ranking,expression:"ranking"}],attrs:{disabled:e.locked,type:"radio",name:"ranking",value:"1"},domProps:{checked:e._q(e.ranking,"1")},on:{change:[function(i){e.ranking="1"},e.updateTable]}}),e._v(" Similarity %\n          ")])]),e._v(" "),a("li",[a("label",[a("input",{directives:[{name:"model",rawName:"v-model",value:e.ranking,expression:"ranking"}],attrs:{disabled:e.locked,type:"radio",name:"ranking",value:"2"},domProps:{checked:e._q(e.ranking,"2")},on:{change:[function(i){e.ranking="2"},e.updateTable]}}),e._v(" N-grams matched\n          ")])]),e._v(" "),a("li",[a("label",[a("input",{directives:[{name:"model",rawName:"v-model",value:e.ranking,expression:"ranking"}],attrs:{disabled:e.locked,type:"radio",name:"ranking",value:"3"},domProps:{checked:e._q(e.ranking,"3")},on:{change:[function(i){e.ranking="3"},e.updateTable]}}),e._v(" Average n-gram ranking\n          ")])])])],1),e._v(" "),a("div",{staticClass:"col"},[a("table",{staticClass:"table table-striped table-sm table-hover"},[a("thead",[a("tr",[a("th",{attrs:{scope:"col"}},[e._v("#")]),e._v(" "),a("th",{attrs:{scope:"col"}},[e._v("Title")]),e._v(" "),a("th",{attrs:{scope:"col"}},[e._v("Artist")]),e._v(" "),1==e.ranking?a("th",{attrs:{scope:"col"}},[e._v("Similarity %")]):e._e(),e._v(" "),2==e.ranking?a("th",{attrs:{scope:"col"}},[e._v("N-grams matched")]):e._e(),e._v(" "),3==e.ranking?a("th",{attrs:{scope:"col"}},[e._v("Average n-gram ranking")]):e._e(),e._v(" "),4==e.ranking?a("th",{attrs:{scope:"col"}},[e._v("Weighted average n-gram ranking")]):e._e()])]),e._v(" "),a("tbody",e._l(e.chart,function(i,t){return a("tr",{key:t,on:{click:function(a){e.$router.push({path:"song/"+i.id})}}},[a("th",{attrs:{scope:"row"}},[e._v(e._s(t+1))]),e._v(" "),a("td",[e._v("\n              "+e._s(i.title)+"\n              "),e.showSimilarities?[a("br"),e._v(" "),a("small",[e._v("Similar to "),a("em",[e._v(e._s(i.top_song.title))]),e._v(" by "+e._s(i.top_song.artist))])]:e._e()],2),e._v(" "),a("td",[e._v(e._s(i.artist))]),e._v(" "),1==e.ranking?a("td",[e._v(e._s(e.formatDecimal(100*i.topSimilarityPercentage)))]):e._e(),e._v(" "),2==e.ranking?a("td",[e._v(e._s(i.ngrams_matched))]):e._e(),e._v(" "),3==e.ranking?a("td",[e._v(e._s(e.formatDecimal(i.averageRanking)))]):e._e(),e._v(" "),4==e.ranking?a("td",[e._v(e._s(e.formatDecimal(i.weightedAverageRanking)))]):e._e()])}),0)])])])])},[],!1,null,null,null);l.options.__file="index.vue";i.default=l.exports}}]);