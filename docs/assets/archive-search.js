document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("#paper-search");
  const input = document.querySelector("#paper-search-input");
  const status = document.querySelector("#paper-search-status");
  const table = document.querySelector("table");

  if (!form || !input || !status || !table || !table.tBodies.length) {
    return;
  }

  const rows = Array.from(table.tBodies[0].rows);
  const normalize = (value) => value.normalize("NFKC").toLocaleLowerCase("ko-KR").trim();

  const search = () => {
    const query = normalize(input.value);
    let matches = 0;

    rows.forEach((row) => {
      const title = normalize(row.cells[1]?.textContent || "");
      const visible = !query || title.includes(query);
      row.hidden = !visible;
      if (visible) {
        matches += 1;
      }
    });

    status.textContent = query
      ? `${matches}개의 논문을 찾았습니다.`
      : `전체 ${rows.length}개의 논문을 표시합니다.`;
  };

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    search();
  });
  form.addEventListener("reset", () => window.setTimeout(search, 0));

  search();
});
