/**
 * @author pjnovas
 */

var ShieldBrick = DrawableElement.extend({
	init: function(options){
		this._super(options);
		
		this.state = 0;
		this.imgsState = options.imgsState;
		this.destroyed = false;
	},
	build: function(){
		
	},
	update: function(){
		
	},
	draw: function(){
		if (!this.destroyed){
			this._super(this.imgsState[this.state]);
	   }
	},
	collided: function(full){
		if (full) this.state = 3;
		else this.state++;

		if (this.state > 2){
			this.destroyed = true;
		}	
	},
	destroy: function(){
		this._super();
	}
});
