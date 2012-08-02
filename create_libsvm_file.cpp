#include <fstream>

using namespace std;

int main(int argc, char const *argv[])
{
    ifstream data;
    ifstream labels;
    ofstream char_recon;

    int num_instances = 2600;
    int num_character = 400;

    float val;

    data.open("data.txt");
    labels.open("labels.txt");
    char_recon.open("char_recon.db");

    for (int i = 0; i < num_instances; ++i)
    {
        labels >> val;
        char_recon << (int) val << "    ";
        for (int j = 0; j < num_character; ++j)
        {
            data >> val;
            char_recon << j + 1 << ":" << (int)val << " ";
        }
        char_recon << endl;
    }

    data.close();
    labels.close();
    char_recon.close();

    return 0;
}