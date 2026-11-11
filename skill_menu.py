"""The skill menu: type / in the chat box and a list of skills pops up above it.

Streamlit's chat box can't show a menu on its own, so we add a small piece of
JavaScript (code that runs in the browser). It watches what's typed in the chat box,
shows matching skills, and fills in the one you click.
If a Streamlit update ever breaks this, typing /skill-name by hand still works.
"""

import json

import streamlit as st

# The browser code. __SKILLS__ is swapped for the real skill list before it's sent.
MENU_SCRIPT = """
<script>
(function () {
  // The latest skill list. Updated every time the app redraws, so new skills show up.
  window.airescentsSkills = __SKILLS__;

  // Only set up the menu once, even though the app redraws many times
  if (window.airescentsSkillMenu) return;
  window.airescentsSkillMenu = true;

  // The menu box itself. It floats above the chat box.
  const menu = document.createElement("div");
  menu.style.cssText = `
    position: fixed; z-index: 1000; display: none;
    background: white; color: #222; border: 1px solid #ddd; border-radius: 8px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.15); padding: 4px; max-height: 260px;
    overflow-y: auto; font-family: inherit; font-size: 14px;`;
  document.body.appendChild(menu);

  // Find Streamlit's chat box (it's redrawn sometimes, so look it up fresh each time)
  function chatBox() {
    return document.querySelector('[data-testid="stChatInputTextArea"]');
  }

  // Put text in the chat box in a way Streamlit notices
  function fillChatBox(box, text) {
    const setValue = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, "value").set;
    setValue.call(box, text);
    box.dispatchEvent(new Event("input", { bubbles: true }));
    box.focus();
  }

  let matches = [];     // the skills currently shown in the menu
  let highlighted = 0;  // which row is highlighted (0 = the top one)

  function menuIsOpen() {
    return menu.style.display === "block";
  }

  function hideMenu() {
    menu.style.display = "none";
  }

  // Fill the chat box with the chosen skill, e.g. "/platform-checkup "
  function pickSkill(skill) {
    fillChatBox(chatBox(), "/" + skill.name + " ");  // the space lets them add e.g. TikTok
    hideMenu();
  }

  // Shade the highlighted row and make sure it's scrolled into view
  function showHighlight() {
    [...menu.children].forEach((row, i) => {
      row.style.background = i === highlighted && matches.length ? "#f0f2f6" : "";
    });
    if (menu.children[highlighted]) menu.children[highlighted].scrollIntoView({ block: "nearest" });
  }

  // Show the skills that match what's been typed so far
  function updateMenu() {
    const box = chatBox();
    const text = box ? box.value : "";

    // Only open when / is the very first character, and only until a space is typed
    // ("/platform-checkup TikTok" means the skill is already chosen)
    if (!text.startsWith("/") || text.includes(" ")) return hideMenu();

    const typed = text.slice(1).toLowerCase();  // what comes after the /
    matches = window.airescentsSkills.filter(s => s.name.toLowerCase().includes(typed));
    highlighted = 0;  // start at the top each time the list changes

    menu.innerHTML = "";
    if (matches.length === 0) {
      const empty = document.createElement("div");
      empty.textContent = "No skills match";
      empty.style.cssText = "padding: 8px 10px; color: #888;";
      menu.appendChild(empty);
    }
    matches.forEach((skill, i) => {
      // One row per skill: the command in bold, its description underneath
      const row = document.createElement("div");
      row.style.cssText = "padding: 8px 10px; border-radius: 6px; cursor: pointer;";
      // Pointing at a row highlights it, so mouse and keyboard always agree
      row.onmouseenter = () => { highlighted = i; showHighlight(); };
      const name = document.createElement("div");
      name.textContent = "/" + skill.name;
      name.style.fontWeight = "600";
      const description = document.createElement("div");
      description.textContent = skill.description;
      description.style.cssText = "color: #666; font-size: 12px;";
      row.append(name, description);
      // mousedown (not click) so the chat box doesn't lose focus first
      row.onmousedown = (event) => {
        event.preventDefault();
        pickSkill(skill);
      };
      menu.appendChild(row);
    });

    // Line the menu up just above the chat box (the whole box, not just the typing area)
    const spot = (box.closest('[data-testid="stChatInput"]') || box).getBoundingClientRect();
    menu.style.left = spot.left + "px";
    menu.style.width = spot.width + "px";
    menu.style.bottom = (window.innerHeight - spot.top + 8) + "px";
    menu.style.display = "block";
    showHighlight();
  }

  // Arrow keys, Enter, Tab and Esc work the menu while it's open.
  // "true" at the end means we see each key before the chat box does,
  // so Enter picks a skill instead of sending the message.
  document.addEventListener("keydown", (event) => {
    if (event.target !== chatBox() || !menuIsOpen()) return;  // menu closed: keys work as normal

    if (event.key === "Escape") {
      hideMenu();
    } else if (matches.length === 0) {
      return;  // "No skills match": nothing to move through or pick, so keys work as normal
    } else if (event.key === "ArrowDown") {
      highlighted = (highlighted + 1) % matches.length;  // past the bottom wraps to the top
      showHighlight();
    } else if (event.key === "ArrowUp") {
      highlighted = (highlighted - 1 + matches.length) % matches.length;  // and the other way
      showHighlight();
    } else if ((event.key === "Enter" && !event.shiftKey) || event.key === "Tab") {
      pickSkill(matches[highlighted]);
    } else {
      return;  // any other key just types as normal
    }
    // We handled this key, so stop the chat box from also acting on it
    event.preventDefault();
    event.stopImmediatePropagation();
  }, true);

  // Check after every keystroke in the chat box
  document.addEventListener("input", (event) => {
    if (event.target === chatBox()) updateMenu();
  });
  // Clicking back into the chat box reopens the menu if a /command is half typed
  document.addEventListener("focusin", (event) => {
    if (event.target === chatBox()) updateMenu();
  });
  // Close the menu when the chat box loses focus (e.g. clicking elsewhere)
  document.addEventListener("focusout", (event) => {
    if (event.target === chatBox()) hideMenu();
  });
  // Keep it lined up if the window is resized
  window.addEventListener("resize", () => {
    if (menu.style.display === "block") updateMenu();
  });
})();
</script>
"""


def show_skill_menu(skills: dict):
    """Add the pop-up skill menu to the page. `skills` comes from load_skills() in app.py."""
    skill_list = [{"name": name, "description": s["description"]} for name, s in skills.items()]
    # "<\\/" stops a skill's text from accidentally ending the <script> early
    skills_json = json.dumps(skill_list).replace("</", "<\\/")
    st.html(MENU_SCRIPT.replace("__SKILLS__", skills_json), unsafe_allow_javascript=True)
