function changeView() {
    let grid = document.getElementById('grid');
    let table = document.getElementById('table');
    if (grid.style.display === 'none') {
        table.style.display = 'none';
        grid.style.display = 'block';
        document.getElementById('btnChangeView').innerHTML = '<i class="fas fa-list"></i>';
    } else {
        table.style.display = 'block';
        grid.style.display = 'none';
        document.getElementById('btnChangeView').innerHTML = '<i class="fas fa-th"></i>';
    }
}

class Stack {
    constructor() {
        this.stack = [];
    }

    add(folderID) {
        this.stack.push(folderID)
    }

    remove() {
        return this.stack.pop()
    }
}

let pile = new Stack()

Dropzone.options.demoUpload = {
    addRemoveLinks: true,
    uploadMultiple: true,
    maxFilesize: 4000,
    parallelUploads: 100,
    autoProcessQueue: false,
    dictRemoveFile: 'Effacer',
    init: function () {
        document.getElementById('loadSingleFile').addEventListener(
            'click', () => {
                this.processQueue();
            }
        );

        this.on('complete', (file) => {
            //this.addRemoveLinks :false;
            setTimeout(() => {
                this.removeFile(file);
            }, 3000);
        });
    },
}

function displayFolderContent(folderID) {
    document.getElementById('folders').style.display = 'none';
    let last = pile.remove();
    if (last) document.getElementById(last).style.display = 'none';
    document.getElementById('folder-content-' + folderID).style.display = 'block';
    pile.add('folder-content-' + folderID)
}

function displayFolderList() {
    let el = pile.remove();
    el.style.display = 'block';
}

let folderLink = document.getElementsByClassName(' folder-link');
for (let i = 0; i < folderLink.length; i++) {
    folderLink[i].addEventListener("click", () => {
            let el = document.getElementsByClassName('active-folder-link');
            let activeFolder = el ? el : null;
            if (activeFolder[0] != null || activeFolder[0] != undefined) {
                activeFolder[0].classList.remove('active-folder-link');
            }
            folderLink[i].classList.add('active-folder-link');

        }
    )
}
Dropzone.options.inFolderUpload = {
    addRemoveLinks: true,
    uploadMultiple: true,
    parallelUploads: 100,
    maxFilesize: 4000,
    autoProcessQueue: false,
    dictRemoveFile: 'Effacer',
    init: function () {
        document.getElementById('loadFileInFolder').addEventListener(
            'click', () => {
                this.processQueue();
            }
        );

        this.on('complete', (file) => {
            //this.addRemoveLinks :false;
            setTimeout(() => {
                this.removeFile(file);
            }, 3000);
        });
    },
}
function filterItems() {
            let searchInput, filter, items, fileTitle, txtValue;
            searchInput = document.getElementById("topbarInputIconLeft");
            filter = searchInput.value.toUpperCase();
            items = document.getElementsByClassName("col-1");

            for (let i = 0; i < items.length; i++) {
                fileTitle = items[i].getElementsByClassName("file-title")[0];
                if (fileTitle) {
                    txtValue = fileTitle.textContent || fileTitle.innerText;
                    if (txtValue.toUpperCase().indexOf(filter) > -1) {
                        items[i].style.display = "";
                    } else {
                        items[i].style.display = "none";
                    }
                }
            }
            for (let i = 0; i < items.length; i++) {
                fileTitle = items[i].getElementsByClassName("folder-title")[0];
                if (fileTitle) {
                    txtValue = fileTitle.textContent || fileTitle.innerText;
                    if (txtValue.toUpperCase().indexOf(filter) > -1) {
                        items[i].style.display = "";
                    } else {
                        items[i].style.display = "none";
                    }
                }
            }
            let tr = document.getElementsByTagName("tr");
            for (let i = 0; i < tr.length; i++) {
                let td = tr[i].getElementsByTagName("td")[0];
                if (td) {
                    txtValue = td.textContent || td.innerText;
                    if (txtValue.toUpperCase().indexOf(filter) > -1) {
                        tr[i].style.display = "";
                    } else {
                        tr[i].style.display = "none";
                    }
                }
            }
        }
function filterTable() {
        let input, filter, table, tr, td, i, txtValue;
        input = document.getElementById("filterInput");
        filter = input.value.toUpperCase();
        table = document.getElementById("membersTable");
        tr = table.getElementsByTagName("tr");
        for (i = 0; i < tr.length; i++) {
            td = tr[i].getElementsByTagName("td")[0];
            if (td) {
                txtValue = td.textContent || td.innerText;
                if (txtValue.toUpperCase().indexOf(filter) > -1) {
                    tr[i].style.display = "";
                } else {
                    tr[i].style.display = "none";
                }
            }
        }
    }