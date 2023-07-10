
export class FileNode {
    public name: string;
    public chain: FileTree[];
    constructor(name: string, chain: FileTree[]) {
        this.name = name;
        this.chain = chain;
    }
}
export class Directory {
    public name: string;
    public chain: FileTree[];
    public children: Record<string, FileTree>;
    constructor(name: string, chain: FileTree[]) {
        this.name = name;
        this.chain = chain;
        this.children = {};
    }
}
export type FileTree = FileNode | Directory;
export const convertFilelistToTree = (filelist: string[]): FileTree => {
    const root = new Directory('root', []);
    const recursivelyPopulateTreeFromDir = (node: Directory, chain: string[]): Directory => {
        if (chain.length === 0) {
            return node;
        }
        const [dir, ...rest] = chain;
        if (node?.children[dir]) {
            return recursivelyPopulateTreeFromDir(node.children[dir] as Directory, rest);
        } else {
            const newDir = { name: dir, chain: [...node.chain, node], children: {} };
            node.children[dir] = newDir;
            return recursivelyPopulateTreeFromDir(newDir, rest);
        }
    }
    filelist.forEach((filepath) => {
        // trace down from root to filepath and add a node
        const chain = filepath.split('/').slice(0, -1);
        const name = filepath.split('/').at(-1);
        const endNode = recursivelyPopulateTreeFromDir(root, chain);
        // add file as file node to the end of the chain
        if (name) {
            const fileNode = new FileNode(name, endNode.chain);
            endNode.children[name] = fileNode;
        }
    });
    return root;
}
