$fn = 48;

union() {
	union() {
		translate(v = [-15, 0, 0]) {
			cube(center = true, size = [10, 5, 3]);
		}
		translate(v = [-10, 0, 0]) {
			difference() {
				cylinder(h = 15, r = 5, center = true);
				cylinder(h = 16, r = 4, center = true);
			}
		}
	}
	union() {
		translate(v = [15, 0, 0]) {
			cube(center = true, size = [10, 5, 3]);
		}
		translate(v = [10, 0, 0]) {
			difference() {
				cylinder(h = 15, r = 5, center = true);
				cylinder(h = 16, r = 4, center = true);
			}
		}
	}
}