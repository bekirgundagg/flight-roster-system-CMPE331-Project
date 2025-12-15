// PİLOTS – hâlihazırda var
export const mockPilots = [
  {
    id: 1,
    name: "George",
    age: 36,
    image: "/images/pilot-george.jpg",
    planes: ["A320"],
    routes: ["Istanbul - New York", "Paris - Rome", "Saville - Tokyo", "Vilnius - Berlin"],
    crew: ["Ava Miller", "Lou Green"]
  },
  {
    id: 2,
    name: "Adam",
    age: 47,
    image: "/images/pilot-adam.jpg",
    planes: ["A320"],
    routes: ["Istanbul - New York", "Paris - Rome"],
    crew: ["Ava Miller", "Lou Green"]
  },
  {
    id: 3,
    name: "Amy",
    age: 28,
    image: "/images/pilot-amy.jpg",
    planes: ["A320"],
    routes: ["Saville - Tokyo", "Vilnius - Berlin"],
    crew: ["Ava Miller", "Lou Green"]
  }
];

// FLIGHT CREW – hâlihazırda var
export const mockCrew = [
  {
    id: 1,
    name: "Ava Miller",
    age: 40,
    role: "Flight Attendant",
    image: "/images/crew-ava.jpg",
    planes: ["A320"],
    flights: ["Istanbul - New York", "Saville - Tokyo"]
  },
  {
    id: 2,
    name: "Lou Green",
    age: 34,
    role: "Cabin Crew",
    image: "/images/crew-lou.jpg",
    planes: ["A320"],
    flights: ["Paris - Rome", "Vilnius - Berlin"]
  }
];

// FLIGHT – hâlihazırda var
export const mockFlights = [
  {
    destination: { city: "Berlin" },
    vehicle_type: { plane_code: "A320" },
    pilots: ["George", "Adam", "Amy"],
    crew: ["Ava Miller", "Lou Green"]
  }
];


// ⬇️⬇️ BUNU DOSYANIN EN ALTINA EKLE (LOGIN İÇİN KULLANILACAK)
// LOGIN USERS
export const mockUsers = [
  { email: "george@skyteam.com", password: "pilot123" },
  { email: "adam@skyteam.com", password: "pilot123" },
  { email: "amy@skyteam.com", password: "pilot123" },
  { email: "ava@skyteam.com", password: "crew123" },
  { email: "lou@skyteam.com", password: "crew123" },
  { email: "admin@skyteam.com", password: "admin123" },
  { email: "guest@skyteam.com", password: "guest123" }
];
