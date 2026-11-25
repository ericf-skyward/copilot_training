const assert = require("node:assert/strict");
const { readFileSync } = require("node:fs");
const { join } = require("node:path");
const test = require("node:test");
const { runInNewContext } = require("node:vm");

class Element {
  constructor() {
    this.children = [];
    this.handlers = {};
    this.value = "";
    this.textContent = "";
    this.classList = { add() {}, remove() {} };
  }

  set innerHTML(value) {
    this.html = value;
    this.children = [];
  }

  get options() {
    return this.children;
  }

  appendChild(child) {
    this.children.push(child);
  }

  replaceChildren(...children) {
    this.children = children;
  }

  setAttribute() {}

  addEventListener(event, handler) {
    this.handlers[event] = handler;
  }
}

async function setup({ rejectSignup = false } = {}) {
  const elements = Object.fromEntries(
    ["activities-list", "activity", "signup-form", "message", "email"].map(
      (id) => [id, new Element()]
    )
  );
  elements.activity.appendChild(new Element());
  elements["signup-form"].reset = () => {
    elements.email.value = "";
    elements.activity.value = "";
  };

  const data = {
    "Chess Club": {
      description: "Chess",
      schedule: "Friday",
      max_participants: 2,
      participants: [],
    },
  };
  let cachedActivities;
  let getCount = 0;
  const fetch = async (url, options = {}) => {
    if (options.method === "POST") {
      if (rejectSignup) {
        return { ok: false, json: async () => ({ detail: "Already signed up" }) };
      }
      data["Chess Club"].participants.push("student@example.com");
      return { ok: true, json: async () => ({ message: "Signed up" }) };
    }

    assert.equal(url, "/activities");
    getCount += 1;
    if (!cachedActivities || options.cache === "no-store") {
      cachedActivities = JSON.parse(JSON.stringify(data));
    }
    return { ok: true, json: async () => cachedActivities };
  };

  let ready;
  const document = {
    getElementById: (id) => elements[id],
    createElement: () => new Element(),
    addEventListener: (_, handler) => { ready = handler; },
  };
  const source = readFileSync(join(__dirname, "../src/static/app.js"), "utf8");
  runInNewContext(source, { document, fetch, console, setTimeout() {} });
  ready();
  await new Promise(setImmediate);
  elements.email.value = "student@example.com";
  elements.activity.value = "Chess Club";
  return { elements, getCount: () => getCount };
}

test("signup refreshes the participant list and availability without cached data", async () => {
  // Arrange
  const { elements, getCount } = await setup();

  // Act
  await elements["signup-form"].handlers.submit({ preventDefault() {} });

  // Assert
  const card = elements["activities-list"].children[0];
  const participants = card.children[0].children[1].children;
  assert.equal(participants[0].children[0].textContent, "student@example.com");
  assert.match(card.html, /1 spots left/);
  assert.equal(getCount(), 2);
  assert.equal(elements.activity.options.length, 2);
  assert.equal(elements.message.textContent, "Signed up");
});

test("failed signup leaves the activity list unchanged", async () => {
  // Arrange
  const { elements, getCount } = await setup({ rejectSignup: true });

  // Act
  await elements["signup-form"].handlers.submit({ preventDefault() {} });

  // Assert
  const card = elements["activities-list"].children[0];
  assert.equal(card.children[0].children[1].textContent, "No participants yet.");
  assert.equal(getCount(), 1);
  assert.equal(elements.message.textContent, "Already signed up");
});
