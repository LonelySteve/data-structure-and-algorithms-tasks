using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MultielementPolynomial
{

    /// <summary>
    /// 多元多项式广义表
    /// </summary>
    public class MPList : IEnumerator
    {
        private List<char> varNames = new List<char>();

        public MPList(char var_name)
        {
            Head = null;
            IsEmpty = true;
            Length = 0;
            VarNames.Add(var_name);
        }
        /// <summary>
        /// 顶级广义表
        /// </summary>
        public MPList RootList { private set; get; }
        /// <summary>
        /// 当前广义表所有变元列表
        /// </summary>
        public List<KeyValuePair<char, MPList>> VarsOrderedDict
        {
            get
            {
                throw new NotImplementedException();
            }
        }
        /// <summary>
        /// 当前广义表变元
        /// </summary>
        public char VarName => VarsOrderedDict[0].Key;
        /// <summary>
        /// 广义表长度
        /// </summary>
        public uint Length { set; get; }
        public uint Depth { set; get; }
        public bool IsEmpty { set; get; }
        /// <summary>
        /// 头结点
        /// </summary>
        public MPNode Head { set; get; }

        /// <summary>
        /// 尾结点
        /// </summary>
        public MPNode Tail { set; get; }

        public object Current => CurrentNode;

        private MPNode CurrentNode { get; set; }

        public void InsertFirst(MPNode node)
        {
            if (Head == null)
            {
                Tail = node;
                node.Next = null;
            }
            else
            {
                node.Next = Head;
            }
            Head = node;
            Length++;
        }

        public void InsertEnd(MPNode node)
        {
            if (Tail == null)
            {
                Tail = Head = node;
            }
            else
            {
                Tail.Next = node;
            }
            node.Next = null;
            Length++;
        }

        public IEnumerator<MPNode> GetEnumerator()
        {
            var cur_node = Head;
            while (cur_node != null)
            {
                yield return cur_node;
                cur_node = cur_node.Next;
            }
        }

        public bool MoveNext()
        {
            if (CurrentNode == null)
            {
                return false;
            }
            CurrentNode = CurrentNode.Next;
            return true;
        }

        public void Reset()
        {
            CurrentNode = Head;
        }

        /// <summary>
        /// 两个多元多项式广义表相乘
        /// </summary>
        /// <param name="l_list"></param>
        /// <param name="r_list"></param>
        /// <returns></returns>
        public static MPList operator *(MPList l_list, MPList r_list)
        {
            _ = l_list ?? throw new ArgumentNullException("l_list");
            _ = r_list ?? throw new ArgumentNullException("r_list");

           var  l_list.VarsOrderedDict.Count ;

            MPList list = new MPList();
            // 相同变元节点之间相乘
            foreach (var kv in l_list.VarsOrderedDict)
            {
                foreach (var node_1 in kv.Value)
                {
                    try
                    {
                        var result = r_list.VarsOrderedDict.Find((KeyValuePair<char, MPList> item) => item.Key == kv.Key);

                        foreach (var node_2 in result.Value)
                        {
                            list.InsertFirst(node_1 * node_2);
                        }
                    }
                    catch (ArgumentNullException)
                    {
                        break;
                    }

                }
            }
 
        }
        /// <summary>
        /// 多元多项式广义表和一个数相乘
        /// </summary>
        /// <param name="l_list"></param>
        /// <param name="num"></param>
        /// <returns></returns>
        public static MPList operator *(MPList l_list, float num)
        {
            throw new NotImplementedException();
        }
        /// <summary>
        /// 两个多元多项式广义表相加
        /// </summary>
        /// <param name="l_list"></param>
        /// <param name="r_list"></param>
        /// <returns></returns>
        public static MPList operator +(MPList l_list, MPList r_list)
        {
            throw new NotImplementedException();
        }
        /// <summary>
        /// 多元多项式广义表和一个数相加
        /// </summary>
        /// <param name="l_list"></param>
        /// <param name="num"></param>
        /// <returns></returns>
        public static MPList operator +(MPList l_list, float num)
        {
            throw new NotImplementedException();
        }
    }
}
