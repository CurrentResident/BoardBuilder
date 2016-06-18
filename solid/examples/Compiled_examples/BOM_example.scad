

union() {
	difference() {
		cube(center = true, size = [30, 10, 5]);
		translate(v = [-10, 0, 0]) {
			translate(v = [0, 0, -0.0100000000]) {
				cylinder(h = 5.0200000000, r = 1.4000000000);
			}
		}
		translate(v = [0, 0, -0.0100000000]) {
			cylinder(h = 5.0200000000, r = 1.4000000000);
		}
		translate(v = [10, 0, 0]) {
			translate(v = [0, 0, -0.0100000000]) {
				cylinder(h = 5.0200000000, r = 1.4000000000);
			}
		}
	}
	translate(v = [-10, 0, 2]) {
		union() {
			cylinder(h = 2.8000000000, r = 2.6500000000);
			translate(v = [0, 0, -12]) {
				cylinder(h = 12, r = 1.4000000000);
			}
		}
	}
	translate(v = [0, 0, 2]) {
		union() {
			cylinder(h = 2.8000000000, r = 2.6500000000);
			translate(v = [0, 0, -16]) {
				cylinder(h = 16, r = 1.4000000000);
			}
		}
	}
	translate(v = [10, 0, 2]) {
		union() {
			cylinder(h = 2.8000000000, r = 2.6500000000);
			translate(v = [0, 0, -12]) {
				cylinder(h = 12, r = 1.4000000000);
			}
		}
	}
	translate(v = [-10, 0, -4.3000000000]) {
		difference() {
			cylinder(h = 2.3000000000, r = 3);
			translate(v = [0, 0, -0.0100000000]) {
				cylinder(h = 2.3200000000, r = 1.4000000000);
			}
		}
	}
	translate(v = [0, 0, -4.3000000000]) {
		difference() {
			cylinder(h = 2.3000000000, r = 3);
			translate(v = [0, 0, -0.0100000000]) {
				cylinder(h = 2.3200000000, r = 1.4000000000);
			}
		}
	}
	translate(v = [10, 0, -4.3000000000]) {
		difference() {
			cylinder(h = 2.3000000000, r = 3);
			translate(v = [0, 0, -0.0100000000]) {
				cylinder(h = 2.3200000000, r = 1.4000000000);
			}
		}
	}
}