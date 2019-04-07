using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MultielementPolynomial
{
    /// <summary>
    /// 节点基类
    /// </summary>
    public class MPNode
    {
        /// <summary>
        /// 系数
        /// </summary>
        public float Coef { get; set; }
        /// <summary>
        /// 广义表
        /// </summary>
        public MPList List { set; get; }
        /// <summary>
        /// 指数
        /// </summary>
        public int Exp { get; set; }
        /// <summary>
        /// 下一个节点
        /// </summary>
        public MPNode Next { get; set; }


        /// <summary>
        /// 两个节点相乘
        /// </summary>
        /// <param name="l_node"></param>
        /// <param name="r_node"></param>
        /// <returns></returns>
        public static MPNode operator *(MPNode l_node, MPNode r_node)
        {
            throw new NotImplementedException();
        }
        /// <summary>
        /// 节点和数相乘
        /// </summary>
        /// <param name="l_node"></param>
        /// <param name="r_node"></param>
        /// <returns></returns>
        public static MPNode operator *(MPNode l_node, float r_node)
        {
            throw new NotImplementedException();
        }

    }
}
